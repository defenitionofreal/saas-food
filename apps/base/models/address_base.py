from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AddressBase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    session_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=255
    )
    city = models.CharField(
        max_length=255
    )
    region = models.CharField(
        max_length=255
    )
    street = models.CharField(
        max_length=255
    )
    building = models.CharField(
        max_length=255
    )
    latitude = models.CharField(
        max_length=255
    )
    longitude = models.CharField(
        max_length=255
    )
    postcode = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    # full string from nominatim api
    display_name = models.CharField(
        max_length=1000,
        blank=True,
        null=True

    )

    def __str__(self):
        return f"id:{self.id}"

    class Meta:
        abstract = True
