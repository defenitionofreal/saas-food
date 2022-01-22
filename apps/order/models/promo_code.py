from django.db import models
from apps.delivery.models.enums import SaleType


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
    sale = models.IntegerField()
    cart_total = models.IntegerField(blank=True, null=True)  # цифра в корзине меньше которой код не применяется
    delivery_free = models.BooleanField(default=False, blank=True, null=True)
    products = models.ManyToManyField("product.Product", blank=True)
    categories = models.ManyToManyField("product.Category", blank=True)
    date_start = models.DateField(blank=True, null=True)
    date_finish = models.DateField(blank=True, null=True)
    code_use = models.IntegerField(blank=True, null=True)
    code_use_by_user = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
