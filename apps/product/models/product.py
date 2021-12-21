from django.db import models

from apps.product.models.enums import WeightUnit


class Product(models.Model):
    """
    Product of institution
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey("product.Category", on_delete=models.PROTECT, related_name="products")
    sticker = models.ForeignKey("product.Sticker", on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    row = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField("media.Image", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    protein = models.FloatField(blank=True)
    fats = models.FloatField(blank=True)
    carbohydrates = models.FloatField(blank=True)
    calories = models.FloatField(blank=True)
    additives = models.ManyToManyField("product.Additive", blank=True)
    modifiers = models.ManyToManyField("product.Modifier", blank=True)
    weight_unit = models.CharField(max_length=50, choices=WeightUnit.choices, default=WeightUnit.GRAM)
    weight = models.FloatField(max_length=50, blank=True)
    cook_time = models.PositiveIntegerField()
    slug = models.SlugField()

    def __str__(self):
        return self.title
