from django.db import models
from django.contrib.auth import get_user_model
from apps.base.models.enums.sms_status import Status
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

# todo: DEL?
class Sms(models.Model):
    sms_aero_id = models.IntegerField(verbose_name="Sms Aero ID", null=True, blank=True)

    # может быть пустым, если пользователя для номера телефона не существует
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Получатель",
        null=True,
        blank=True,
        related_name="recipient",
    )
    phone = PhoneNumberField(verbose_name="Номер телефона получателя")

    # если пустой, то значит система
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Отправитель",
        null=True,
        blank=True,
        related_name="sender",
    )
    text = models.TextField(verbose_name="Текст SMS")

    # None означает, что сообщение ещё не было передано в SmsAero
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=None,
        verbose_name="Статус",
        blank=True,
        null=True,
    )
    status_text = models.TextField(
        verbose_name="Статус-сообщение",
        blank=True,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = "Сообщение SMS Aero"
        verbose_name_plural = "Сообщения SMS Aero"

    def __str__(self):
        return self.text
