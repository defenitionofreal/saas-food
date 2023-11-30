from django.db import models
from apps.payment.models.enums import PaymentType
from django.contrib.auth import get_user_model

User = get_user_model()

# TODO: может автоматом создавать все способы со старта так же как дни недели? или permission?
class PaymentTypeInstitution(models.Model):
    """
    Organization could create there payment types
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="payment_type"
    )
    type = models.CharField(
        max_length=20,
        choices=PaymentType.choices
    )

    def __str__(self):
        return f"{self.institutions.values_list('title',flat=True)}|{self.type}"
