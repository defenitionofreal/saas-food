from django.contrib.auth import get_user_model
from celery import shared_task

from apps.base.services.sms_aero import SendSms, PhoneNumber


@shared_task
def send_sms_task(phone, text, sender_id=None):
    _validate_phone_number(phone)
    if sender_id:
        sender = get_user_model().objects.filter(id=sender_id).first()
    else:
        # система
        sender = None
    # print для разарботки, _send_sms для отправки реальной смс
    # TODO: добавить функционал, который по settings.dev/prod/local
    #  определяет отправить реальную смс или нет
    print("tasks print", phone, text, sender)
    #_send_sms(phone, text, sender=sender)


def _send_sms(phone, text, sender=None):
    sms = SendSms(phone, text, sender=sender)
    response = sms.call()
    print("_send_sms", response)
    if not response["success"]:
        raise ValueError(f"Failed to send sms {text} for phone number {phone} with error {response}")


def _validate_phone_number(phone):
    phone = PhoneNumber(phone)
    if not phone.is_valid():
        raise ValueError(f"Phone number {str(phone)} is not valid")
