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
    item = models.ForeignKey("product.Product",
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    modifier = models.ForeignKey("product.ModifierPrice",
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)
    additives = models.ManyToManyField("product.Additive",
                                       blank=True)
    quantity = models.PositiveIntegerField(default=1)
    item_hash = models.CharField(max_length=255,
                                 blank=True,
                                 null=True)

    def __str__(self):
        return f'{self.item}, {self.quantity}'

    @property
    def get_item_price(self):
        price = self.item.price
        if self.modifier:
            price = self.modifier.price
        price += sum(additive.price for additive in self.additives.only("price"))
        return price

    @property
    def get_total_item_price(self):
        product_price = self.get_item_price
        quantity = self.quantity
        total_price = (product_price * quantity)
        return Decimal(total_price)
