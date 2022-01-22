from django.db import models
from apps.product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    customer = models.ForeignKey(
        User,
        related_name='items',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cart = models.ForeignKey("order.Cart", on_delete=models.CASCADE, null=True,
                             blank=True, related_name="products_cart")
    product = models.ForeignKey(
        Product,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_single_item_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f'{self.product.title}, {self.quantity}, {self.get_single_item_total}'
