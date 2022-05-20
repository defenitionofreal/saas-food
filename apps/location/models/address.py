from django.db import models


class Address(models.Model):
    city = models.ForeignKey("location.City", on_delete=models.CASCADE)
    region = models.ForeignKey("location.Region", on_delete=models.CASCADE)
    street = models.ForeignKey("location.Street", on_delete=models.CASCADE)
    building = models.CharField(max_length=255)
    office = models.CharField(max_length=255, blank=True)
    floor = models.CharField(max_length=255, blank=True)
    # latitude
    # longitude

    def __str__(self):
        return f"{self.city} {self.region} {self.street} {self.street}\
                 {self.building} {self.office}"
