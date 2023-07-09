from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    """
    Product of institution
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="products",
        blank=True
    )
    category = models.ForeignKey(
        "product.Category",
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )
    stickers = models.ManyToManyField(
        "product.Sticker",
        blank=True
    )
    additives = models.ManyToManyField(
        "product.CategoryAdditive",
        blank=True,
        related_name="product_additives"
    )
    modifiers = models.ManyToManyField(
        "product.Modifier",
        blank=True,
        related_name="product_modifiers"
    )
    is_active = models.BooleanField(default=False)
    row = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField("media.Image", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2,
                                    blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    cook_time = models.PositiveIntegerField()
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title
