from django.db import models


class MinCartCost(models.Model):
    """
    Minimal cart price value to checkout
    """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        blank=True,
        related_name="min_cart_cost"
    )
    cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.cost} на {self.institution}'
