from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ExtraPhone(models.Model):
    """ additional phones for institution """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        blank=True,
        related_name="extra_phone"
    )
    phone = PhoneNumberField()
    position = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
