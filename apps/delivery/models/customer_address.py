from django.db import models
from apps.base.models import AddressBase


class CustomerAddress(AddressBase):
    office = models.CharField(
        max_length=255,
        blank=True,
        null=True

    )
    floor = models.CharField(
        max_length=255,
        blank=True,
        null=True

    )
    intercom = models.CharField(
        max_length=255,
        blank=True,
        null=True

    )
    entrance = models.CharField(
        max_length=255,
        blank=True,
        null=True

    )
    comment = models.CharField(
        max_length=255,
        blank=True,
        null=True

    )
    is_main = models.BooleanField(
        default=False
    )
    is_house = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"id:{self.id} | г. {self.city}, {self.region}, ул. {self.street}\
                 д. {self.building} кв.{self.office} этаж {self.floor}"
