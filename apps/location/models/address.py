from django.db import models


class Address(models.Model):
    # country ? postcode ?
    city = models.CharField(max_length=255)
    # region / state
    region = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=255)
    office = models.CharField(max_length=255, blank=True)
    floor = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    # full string from nominatim api
    display_name = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"id:{self.id} | г. {self.city}, {self.region}, ул. {self.street}\
                 д. {self.building} кв.{self.office} этаж {self.floor}"
