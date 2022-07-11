from django.db import models
from django.contrib.auth import get_user_model

from apps.order.services.math_utils import get_absolute_from_percent_and_total

User = get_user_model()

# TODO: institution ManyToMany
class Bonus(models.Model):
    """
    Model for a organization
    Where organization set there rules for a client
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="bonuses")
    is_active = models.BooleanField(default=False)
    write_off = models.PositiveIntegerField()  # max discount, % from order cost
    accrual = models.PositiveIntegerField()  # amount to get to customer after order is done, % from order cost
    is_promo_code = models.BooleanField(default=False)
    is_registration_bonus = models.BooleanField(default=False)
    # TODO: добавить функций для бонуса при регистрации
    registration_bonus = models.PositiveIntegerField(blank=True, null=True)  # $

    def __str__(self):
        return f'{self.institution.domain} - write off: {self.write_off} / accrual: {self.accrual}'

    def get_write_off_absolute_amount(self, total_cart_price):
        return get_absolute_from_percent_and_total(self.write_off, total_cart_price)


class UserBonus(models.Model):
    """
    Model for a customer
    Where we can detect and count his bonuses
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="user_bonuses")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             blank=True)
    bonus = models.PositiveIntegerField()

    def write_off_bonus_amount(self, amount):
        amount = amount if amount < self.bonus else self.bonus
        self.bonus -= amount
        self.save()

    def __str__(self):
        return f'{self.institution.domain}: {self.user.phone} with {self.bonus} points'
