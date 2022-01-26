from django.db import models


class MinCartCost(models.Model):
    """
    Minimal cart price value to checkout
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="min_cart_value")
    cost = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.cost} на {self.institution}'
