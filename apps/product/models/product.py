from django.db import models

from apps.product.models.enums import WeightUnit


class Product(models.Model):
    """
    Product of institution
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE, related_name="products")
    sticker = models.ForeignKey("product.Sticker", on_delete=models.CASCADE, related_name="products")
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField("media.Image", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    protein = models.CharField(max_length=255)
    fats = models.CharField(max_length=255)
    carbohydrates = models.CharField(max_length=255)
    calories = models.CharField(max_length=255)
    additives = models.ManyToManyField("product.Additive", blank=True)
    #modifiers = models.ManyToManyField("product.Modifier", blank=True)
    weight_unit = models.CharField(max_length=50, choices=WeightUnit.choices)
    weight = models.CharField(max_length=50, blank=True)
    cook_time = models.IntegerField()
    slug = models.SlugField()

    def __str__(self):
        return self.title
