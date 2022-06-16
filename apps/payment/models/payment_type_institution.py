from django.db import models
from apps.payment.models.enums import PaymentType
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentTypeInstitution(models.Model):
    """
    Organization could create there payment types
    """
    institution = models.ManyToManyField("company.Institution",
                                         related_name="payment_type")
    type = models.CharField(max_length=20,
                            choices=PaymentType.choices,
                            default=PaymentType.ONLINE)

    def __str__(self):
        return f"{self.institution.values_list('title',flat=True)}|{self.type}"
