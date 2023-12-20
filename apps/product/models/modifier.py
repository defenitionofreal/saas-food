from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from apps.product.models import (
        ModifierPrice, NutritionalValue, Weight
    )

User = get_user_model()


class Modifier(models.Model):
    """
    Modifier of the product
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="modifiers",
        blank=True
    )
    title = models.CharField(max_length=255)

    def price(self, product_id) -> Optional[ModifierPrice]:
        return self.modifiers_price.filter(product_id=product_id).first()

    def nutrition(self, product_id) -> Optional[NutritionalValue]:
        return self.nutritional_values.filter(product_id=product_id).first()

    def weight(self, product_id) -> Optional[Weight]:
        return self.weights.filter(product_id=product_id).first()

    def __str__(self):
        return self.title
