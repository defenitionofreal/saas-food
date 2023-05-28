from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ModifierPrice(models.Model):
    """
    Modifier price of the product
    """
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE,
                                related_name="modifiers_price")
    modifier = models.ForeignKey("product.Modifier", on_delete=models.CASCADE,
                                 related_name="modifiers_price")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'id:{self.id}: {self.product.title}, {self.modifier} = {self.price}'
