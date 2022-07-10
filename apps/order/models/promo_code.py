from django.db import models
from apps.delivery.models.enums import SaleType
from django.contrib.auth import get_user_model

User = get_user_model()


# TODO: institution ManyToMany
class PromoCode(models.Model):
    """
    Promo code model for orders
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="promocode")
    title = models.CharField(max_length=100)
    code_type = models.CharField(max_length=20, choices=SaleType.choices)
    code = models.CharField(max_length=10)
    sale = models.PositiveIntegerField()
    cart_total = models.PositiveIntegerField(blank=True, null=True)
    delivery_free = models.BooleanField(default=False, blank=True, null=True)
    products = models.ManyToManyField("product.Product", blank=True)
    categories = models.ManyToManyField("product.Category", blank=True)
    date_start = models.DateField(blank=True, null=True)
    date_finish = models.DateField(blank=True, null=True)
    code_use = models.PositiveIntegerField(blank=True, null=True)
    code_use_by_user = models.PositiveIntegerField(blank=True, null=True)  # total uses by specific user
    num_uses = models.PositiveIntegerField(default=0, editable=False)  # total uses across all users
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PromoCodeUser(models.Model):
    """
    Model to tie coupon and a user together.
    So we can check how many times coupon have been used by user.
    """
    code = models.ForeignKey(PromoCode, related_name='users',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    num_uses = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f'{self.user.phone}: {self.code}'
