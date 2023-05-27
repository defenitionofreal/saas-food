from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Requisites(models.Model):
    """
    Institution paying requisites
    """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        blank=True,
        related_name="requisites"
    )
    name = models.CharField(max_length=255)
    inn = models.IntegerField()
    kpp = models.IntegerField()
    ogrn = models.IntegerField()
    address = models.ForeignKey(
        "location.Address",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+"
    )
    bank = models.CharField(max_length=255)
    bik = models.IntegerField()
    correspondent_account = models.IntegerField()
    checking_account = models.CharField(max_length=255)
    phone = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return str(self.user.email) if self.user.email else str(self.id)
