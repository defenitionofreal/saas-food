from django.db import models


class NutritionalValue(models.Model):
    """ Nutritional value per 100 g for a product or modified product """
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.CASCADE,
        related_name="nutritional_values"
    )
    modifier = models.ForeignKey(
        "product.Modifier",
        on_delete=models.CASCADE,
        related_name="nutritional_values",
        blank=True,
        null=True
    )
    protein = models.FloatField(blank=True, null=True)
    fats = models.FloatField(blank=True, null=True)
    carbohydrates = models.FloatField(blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
