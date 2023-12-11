from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PromoCodeUser(models.Model):
    """
    Model to tie coupon and a user together.
    So we can check how many times coupon have been used by user.
    """
    code = models.ForeignKey(
        "order.PromoCode",
        related_name='users',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    num_uses = models.PositiveIntegerField(
        default=0,
        editable=False
    )

    def __str__(self):
        return f'{self.user.phone}: {self.code}'
