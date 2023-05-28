from django.db import models
from apps.product.models.enums import WeightUnit


class Weight(models.Model):
    """ Weight for product or modified product """
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="weights"
    )
    modifier = models.ForeignKey(
        "product.Modifier",
        on_delete=models.CASCADE,
        related_name="weights",
        blank=True,
        null=True
    )
    weight_unit = models.CharField(
        max_length=50,
        choices=WeightUnit.choices,
        default=WeightUnit.GRAM
    )
    weight = models.FloatField(max_length=50)
