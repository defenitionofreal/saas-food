from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from dateutil.parser import parse

from django_redis import get_redis_connection

from apps.base.models.auth_code import AuthCode

User = get_user_model()


def send_auth_code(phone, phones_count_prefix):
    from apps.base.tasks import send_sms_task
    resending_time = _validate_is_ready_to_sending(phone, phones_count_prefix)
    msg = f"Код для входа - {_create_authentication_code(phone)}. Добро пожаловать на site.com"
    # print("msg:", msg)
    send_sms_task.delay(phone, msg)
    return resending_time


def _validate_is_ready_to_sending(phone, phones_count_prefix):
    client = get_redis_connection()

    if _is_many_phone_numbers_used(client, phones_count_prefix, phone):
        raise ValueError(f"Много использованно телефонов для {phones_count_prefix}")

    resending_time, is_created = _get_resending_time(client, phone)

    if not is_created and _is_wait_resending(resending_time):
        raise ValueError(f"На данный номер телефона {phone} уже выслан код")

    return resending_time


def _is_wait_resending(resending_time):
    return resending_time > now()


def _get_resending_time(connection, phone):
    resend_key = f"SEND_{phone}"
    serialized_time = connection.get(resend_key)

    if serialized_time:
        sending_time = parse(serialized_time)
        is_created = False
    else:
        sending_time = now()
        connection.set(
            resend_key,
            sending_time.isoformat(),
            settings.AUTHENTICATION_SEND_CODE_WINDOW,
        )
        is_created = True

    resending_time = sending_time + timedelta(seconds=settings.AUTHENTICATION_SEND_CODE_WINDOW)

    return resending_time, is_created


def _is_many_phone_numbers_used(connection, phones_count_prefix, phone):
    """
    Counting phones from one IP address
    """
    phones_count = len(connection.keys(f"{phones_count_prefix}*"))
    if phones_count < settings.AUTHENTICATION_PHONE_NUMBERS_COUNT_FROM_IP:
        is_many_phone_numbers_used = False
        used_phone_key = f"{phones_count_prefix}{phone}"
        connection.set(
            used_phone_key,
            now().isoformat(),
            settings.AUTHENTICATION_PHONE_NUMBERS_EXPIRED_FROM_IP,
        )
    else:
        is_many_phone_numbers_used = True
    return is_many_phone_numbers_used


def _create_authentication_code(phone):
    """
    Generate CODE
    """
    user, created = User.objects.get_or_create(phone=phone)
    code = AuthCode.objects.generate(user)  # тут падает
    return code.code
