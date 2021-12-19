from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Requisites(models.Model):
    """
    Institution paying requisites
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="requisites")
    name = models.CharField(max_length=255)
    inn = models.IntegerField()
    kpp = models.IntegerField()
    ogrn = models.IntegerField()
    address = models.ForeignKey("location.Address", on_delete=models.SET_NULL, null=True, related_name="+")
    bank = models.CharField(max_length=255)
    bik = models.IntegerField()
    correspondent_account = models.IntegerField()
    checking_account = models.CharField(max_length=255)
    phone = PhoneNumberField()  # списком
    email = models.EmailField()

    def __str__(self):
        return self.institution
