from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bonus(models.Model):
    """
    Model for a organization
    Bonuses for a client
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="bonuses")
    is_active = models.BooleanField(default=False)
    write_off = models.PositiveIntegerField()  # %
    accrual = models.PositiveIntegerField()  # %
    is_promo_code = models.BooleanField(default=False)
    is_registration_bonus = models.BooleanField(default=False)
    registration_bonus = models.PositiveIntegerField()  # $

    def __str__(self):
        return self.institution


class UserBonus(models.Model):
    """
    Model for a customer
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="user_bonuses")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bonus = models.PositiveIntegerField()

