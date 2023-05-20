from django.conf import settings
from django.contrib.auth import get_user_model
from re import sub
from enum import Enum
from urllib.parse import quote

import requests


# https://smsaero.ru/description/api/ Проверка статусов сообщений
# Статус сообщения (0 — в очереди, 1 — доставлено, 2 — не доставлено,
# 3 — передано, 8 — на модерации, 6 — сообщение отклонено,
# 4 — ожидание статуса сообщения)
class AwaitStatuses(Enum):
    ENQUEUED = 0
    SENT = 3
    MODERATION = 8
    AWAITING_STATUS = 4


class FailStatuses(Enum):
    NOT_DELIVERED = 2
    DISMISSED = 6


class SuccessStatuses(Enum):
    DELIVERED = 1


class SendSms(object):
    """
    Отправка смс
    """
    channels = ["INFO", "INTERNATIONAL", "DIRECT", "SERVICE", "FREE SIGN"]

    # TODO: поменять chanel на SERVICE,
    #  SERVICE использовать можно только с платной подписью
    def __init__(self, phone, text, channel="FREE SIGN", sender=None):
        self.phone = phone
        self.text = text
        if channel not in self.channels:
            raise Exception("[SMS_API] : Channel not exist")
        self.channel = channel

        user = get_user_model().objects.filter(phone=phone).first()
        # self.sms = Sms.objects.create(
        #     recipient=user,
        #     phone=phone,
        #     sender=sender,
        #     text=text,
        # )

    def call(self):
        response = requests.get(self._validation_request_url()).json()
        print("celery response:", response)
        self.sms.sms_aero_id = response["data"]["id"]
        self.sms.status = response["data"]["status"]
        self.sms.status_text = response["data"]["extendStatus"]
        self.sms.save()
        return response

    def _validation_request_url(self):
        request_url = "https://{email}:{api_key}@{api_url}sms/send?number={phone}&text={text}&sign={sign}&channel={channel}".format(
            email=settings.SMS_AERO_API_EMAIL,
            api_key=settings.SMS_AERO_API_KEY,
            api_url=settings.SMS_AERO_API_URL,
            phone=str(self.phone),
            text=quote(self.text),
            sign=settings.SMS_AERO_API_SIGN,
            channel=self.channel,
        )
        return request_url


class PhoneNumber(object):
    """
    Определение оператора
    """
    def __init__(self, phone):
        self.phone = self.__normalize(phone)

    def is_valid(self):
        response = requests.get(self.__validation_request_url()).json()
        return response["success"]

    def format(self):
        return "+{country_code} ({operator_code}) {part1}-{part2}-{part3}".format(
            country_code=self.phone[0],
            operator_code=self.phone[1:4],
            part1=self.phone[4:7],
            part2=self.phone[7:9],
            part3=self.phone[9:],
        )

    def __str__(self):
        return self.format()

    def __normalize(self, phone):
        normalize_number = sub(r"\D", r"", phone)
        return normalize_number

    def __validation_request_url(self):
        request_url = (
            "https://{email}:{api_key}@{api_url}number/operator?number={phone}".format(
                email=settings.SMS_AERO_API_EMAIL,
                api_key=settings.SMS_AERO_API_KEY,
                api_url=settings.SMS_AERO_API_URL,
                phone=self.phone,
            )
        )
        return request_url
