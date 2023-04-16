from django.db import models
from apps.que.models.enums import QueStatus


class Que(models.Model):
    """
    Queue model for order status
    """
    order = models.ForeignKey(
        "order.Cart",
        on_delete=models.CASCADE,
        related_name="que"
    )
    status = models.CharField(
        max_length=20,
        choices=QueStatus.choices,
        default=QueStatus.PROCESSING
    )
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def customer_name(self):
        return self.order.name if self.order.name else None

    @property
    def code(self):
        return self.order.code if self.order.code else None

    # todo: в методе save определять position при нужных статусах
