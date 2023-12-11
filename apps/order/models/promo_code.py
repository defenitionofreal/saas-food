from django.db import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from apps.delivery.models.enums import SaleType

User = get_user_model()


class PromoCode(models.Model):
    """
    Promo code model for orders. User is an owner not a customer.
    """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        blank=True,
        related_name="promocode"
    )
    title = models.CharField(max_length=100)
    code_type = models.CharField(max_length=20, choices=SaleType.choices)
    code = models.CharField(max_length=10)
    sale = models.PositiveIntegerField()
    cart_total = models.PositiveIntegerField(default=0)
    delivery_free = models.BooleanField(default=False)
    products = models.ManyToManyField("product.Product", blank=True)
    categories = models.ManyToManyField("product.Category", blank=True)
    date_start = models.DateField(blank=True, null=True)
    date_finish = models.DateField(blank=True, null=True)
    code_use = models.PositiveIntegerField(default=0)
    code_use_by_user = models.PositiveIntegerField(default=0)
    num_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.code_type == SaleType.PERCENT and self.sale > 100:
            raise ValidationError(
                {"detail": "Sale cannot be greater than 100 for percent type"}
            )

    def __str__(self):
        return self.title
