from django.db import models
from django.contrib.auth import get_user_model
from apps.base.models import SecureCharField


User = get_user_model()


class YooMoney(models.Model):
    """
    Model for organisation wallet id
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="yoomoney"
    )
    wallet = SecureCharField(unique=True)

    def __str__(self):
        return f"{self.user}| {self.wallet}"
