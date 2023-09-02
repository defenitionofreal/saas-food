from django.db import models
from apps.base.models import AddressBase


class InstitutionAddress(AddressBase):
    institution = models.ForeignKey(
        "company.Institution",
        on_delete=models.CASCADE
    )
    def __str__(self):
        return f"id:{self.id} | г. {self.city}, {self.region}, ул. {self.street}\
                 д. {self.building}"
