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
    inn = models.CharField(max_length=255)
    kpp = models.CharField(max_length=255)
    ogrn = models.CharField(max_length=255)
    address = models.TextField()
    bank = models.CharField(max_length=255)
    bik = models.CharField(max_length=255)
    correspondent_account = models.CharField(max_length=255)
    checking_account = models.CharField(max_length=255)
    phone = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return str(self.user.email) if self.user.email else str(self.id)
