from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class YooMoney(models.Model):
    """
    Model for organisation wallet id
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    wallet = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}| {self.wallet}"
