import datetime

from apps.delivery.models.enums import SaleType


def get_today_date():
    return datetime.datetime.now().date()


class PromoCodeHelper:
    def __init__(self, promo_code):
        self.promo_code = promo_code

    def __str__(self):
        if self.is_valid:
            return self.promo_code.title

    @property
    def is_valid(self) -> bool:
        return self.promo_code is not None

    @property
    def is_active(self) -> bool:
        if self.is_valid:
            return self.promo_code.is_active

    @property
    def sale(self) -> [int, None]:
        if self.is_valid:
            return self.promo_code.sale

    @property
    def cart_total(self) -> [int, None]:
        if self.is_valid:
            return self.promo_code.cart_total

    @property
    def code_type(self) -> [SaleType, None]:
        if self.is_valid:
            return self.promo_code.code_type

    @property
    def is_absolute_sale(self) -> bool:
        return self.code_type == SaleType.ABSOLUTE

    @property
    def is_percent_sale(self) -> bool:
        return self.code_type == SaleType.PERCENT

    @property
    def has_num_uses_left(self) -> bool:
        if not self.is_valid:
            return False
        max_num_uses = self.promo_code.code_use
        current_num_uses = self.promo_code.num_uses
        if not max_num_uses:
            return True
        return max_num_uses > current_num_uses

    def can_be_used_on_day_by_start_date(self, date) -> bool:
        if not self.is_valid:
            return False
        date_start = self.promo_code.date_start
        if not date_start:
            return True
        return date >= date_start

    def can_be_used_on_day_by_finish_date(self, date) -> bool:
        if not self.is_valid:
            return False
        date_finish = self.promo_code.date_finish
        if not date_finish:
            return True
        return date < date_finish

    @property
    def can_be_used_today_by_start_date(self) -> bool:
        return self.can_be_used_on_day_by_start_date(get_today_date())

    @property
    def can_be_used_today_by_finish_date(self) -> bool:
        return self.can_be_used_on_day_by_finish_date(get_today_date())

    def can_be_used_by_cart_total(self, cart_total_price) -> bool:
        if not self.is_valid:
            return False
        cart_total = self.cart_total
        if not cart_total:
            return True
        return cart_total_price >= cart_total

    def increase_num_uses(self):
        if self.is_valid:
            self.promo_code.num_uses += 1
            self.promo_code.save()

    def can_be_used_by_user_with_use_count(self, use_count) -> bool:
        if not self.is_valid:
            return False
        max_uses_by_user = self.promo_code.code_use_by_user
        if not max_uses_by_user:
            return True
        return max_uses_by_user > use_count
