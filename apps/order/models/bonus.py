from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bonus(models.Model):
    """
    Model for a organization
    Where organization set there rules for a client
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="bonuses")
    is_active = models.BooleanField(default=False)
    write_off = models.PositiveIntegerField()  # %
    accrual = models.PositiveIntegerField()  # %
    is_promo_code = models.BooleanField(default=False)
    is_registration_bonus = models.BooleanField(default=False)
    registration_bonus = models.PositiveIntegerField(blank=True, null=True)  # $

    def __str__(self):
        return f'{self.institution.domain} - write off: {self.write_off} / accrual: {self.accrual}'


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

    def __str__(self):
        return f'{self.institution.domain}: {self.user.email} with {self.bonus} points'
