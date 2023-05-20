from django.db import models
from django.contrib.auth import get_user_model
from apps.sms.models.enums.status import Status

User = get_user_model()


class SmsLog(models.Model):
    sms_id = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )
    # может быть пустым, если пользователя для номера телефона не существует
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sms_recipient",
    )
    phone = models.CharField(
        max_length=100
    )
    # если пустой, то значит система
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sms_sender",
    )
    text = models.TextField()
    # None означает, что сообщение ещё не было передано
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=None,
        verbose_name="Статус",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Sms Log"
        verbose_name_plural = "Sms Logs"

    def __str__(self):
        return self.text
