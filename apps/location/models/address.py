from django.db import models


class Address(models.Model):
    city = models.ForeignKey("apps.location.City", on_delete=models.CASCADE)
    region = models.ForeignKey("apps.location.Region", on_delete=models.CASCADE)
    street = models.ForeignKey("apps.location.Street", on_delete=models.CASCADE)
    building = models.CharField(max_length=255)
    office = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.city} {self.region} {self.street} {self.street} {self.building} {self.office}"
