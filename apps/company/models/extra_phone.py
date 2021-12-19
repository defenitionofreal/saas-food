from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ExtraPhone(models.Model):
    """ additional phones for institution """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="extra_phone")
    phone = PhoneNumberField()
    position = models.CharField(max_length=255, blank=True)
