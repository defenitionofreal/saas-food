from django.conf import settings
from random import randint
import requests

active_codes = []


def _create_authentication_code():
    attempts_count = 0

    generated_code = None
    while attempts_count < 10 and not generated_code:
        code = randint(1000, 9999)
        if str(code) not in active_codes:
            active_codes.append(str(code))
            generated_code = code
        attempts_count += 1

    if attempts_count >= 10 or not generated_code:
        raise f"Exceeded max count of generate code attemts {settings.MAX_GENERATE_ATTEMPTS_COUNT}"

    return generated_code


def _validation_request_url():
    request_url = "https://{email}:{api_key}@{api_url}sms/send?number={phone}&text={text}&sign={sign}&channel={channel}".format(
        email="flavors@inbox.ru",
        api_key="5bTsLKFrFdxkIhneppvWCIg6gU",
        api_url="gate.smsaero.ru/v2/",
        phone=str("79184333353").replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', ''),
        text=f"{_create_authentication_code()}",
        sign="SMS Aero",
        channel="FREE SIGN",
    )
    return request_url


requests.get(_validation_request_url())
