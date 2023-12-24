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
    # todo: modifiers используется пока как одна группа,
    #  но нужно будет делать несколько групп модификаторов на продукт.
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
    def get_item_price(self) -> Decimal:
        price = self.modifier.price if self.modifier else self.item.price
        price += sum(additive.price for additive in self.additives.only("price"))
        return Decimal(price)

    @property
    def get_total_item_price(self) -> Decimal:
        return Decimal(self.get_item_price * self.quantity)
