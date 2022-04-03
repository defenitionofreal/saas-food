from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CartProduct(models.Model):
    """A model that contains data for a cart product."""
    cart = models.ForeignKey("order.Cart", on_delete=models.CASCADE, related_name="cart_products")
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.RESTRICT,
        related_name="cart_products",
    )
    modifiers = models.ManyToManyField("product.Modifier", blank=True, related_name="cart_products")
    additives = models.ManyToManyField("product.Additive", blank=True, related_name="cart_products")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_coast = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.title}, {self.quantity}"
