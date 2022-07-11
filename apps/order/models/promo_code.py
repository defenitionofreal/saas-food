from django.db import models
from apps.delivery.models.enums import SaleType
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


def get_today_date():
    return datetime.datetime.now().date()


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

    @property
    def is_absolute_sale(self):
        return self.code_type == SaleType.ABSOLUTE

    @property
    def is_percent_sale(self):
        return self.code_type == SaleType.PERCENT

    @property
    def has_num_uses_left(self):
        if not self.code_use:
            return True
        return self.code_use > self.num_uses

    def can_be_used_on_day_by_start_date(self, date):
        if not self.date_start:
            return True
        return date >= self.date_start

    def can_be_used_on_day_by_finish_date(self, date):
        if not self.date_finish:
            return True
        return date < self.date_finish

    @property
    def can_be_used_today_by_start_date(self):
        return self.can_be_used_on_day_by_start_date(get_today_date())

    @property
    def can_be_used_today_by_finish_date(self):
        return self.can_be_used_on_day_by_finish_date(get_today_date())

    def can_be_used_by_cart_total(self, cart_total_price):
        if not self.cart_total:
            return True
        return cart_total_price >= self.cart_total

    def increase_num_uses(self):
        self.num_uses += 1
        self.save()

    def can_be_used_by_user_with_use_count(self, use_count):
        if not self.code_use_by_user:
            return True
        return self.code_use_by_user > use_count


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

    @property
    def can_use_this_code(self):
        m: PromoCode = self.code
        return m.can_be_used_by_user_with_use_count(self.num_uses)

    def increase_num_uses(self):
        self.num_uses += 1
        self.save()
