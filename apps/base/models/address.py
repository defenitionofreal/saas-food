from django.db import models


class AddressModel(models.Model):
    city = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    building = models.CharField(max_length=255, blank=True)
    office = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.city} {self.region} {self.street} {self.street} " \
               f"{self.building} {self.office}"

    class Meta:
        abstract = True
