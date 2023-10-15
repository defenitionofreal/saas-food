from django.db import models
from apps.base.models.custom_user import CustomUser


class YandexGeocoderToken(models.Model):
    user = models.ForeignKey(
        CustomUser,
        limit_choices_to={"is_organization": True},
        on_delete=models.CASCADE
    )
    # todo: tokenize it
    api_key = models.CharField(
        max_length=500,
        unique=True
    )

    def save(self, *args, **kwargs):
        if self.user.is_organization:
            super(YandexGeocoderToken, self).save(*args, **kwargs)
        else:
            raise ValueError('Related user has to be an organization.')
