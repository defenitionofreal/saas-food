from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey("order.Cart",
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name="products_cart")
    product = models.JSONField(default=dict)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product}, {self.quantity}'

    @property
    def get_additives(self):
        return self.product["additives"]

    @property
    def get_modifiers(self):
        return self.product["modifiers"]

    @property
    def get_total_item_price(self):
        product_price = self.product["price"]
        if self.product["modifiers"]:
            product_price = self.product["modifiers"]["price"]
        if self.product["additives"]:
            for i in self.product["additives"]:
                product_price += i["price"]
        quantity = self.quantity
        total_price = (product_price * quantity)

        return Decimal(total_price)
