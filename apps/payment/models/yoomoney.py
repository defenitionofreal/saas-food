from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class YooMoney(models.Model):
    """
    Model for organisation wallet id
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="yoomoney")
    wallet = models.CharField(max_length=255)
    #TODO: (yoomoney) нахер не надо три поля ниже
    client_id = models.CharField(max_length=1000)
    oauth_key = models.CharField(max_length=1000)
    is_test = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}| {self.wallet}"
