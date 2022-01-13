from django.db import models


class Bonus(models.Model):
    """
    Bonuses for a client
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="bonuses")
    is_active = models.BooleanField(default=False)
    write_off = models.PositiveIntegerField()  # %
    accrual = models.PositiveIntegerField()  # %
    is_promo_code = models.BooleanField(default=False)  # можно ли использовать с промокодом
    is_registration_bonus = models.BooleanField(default=False)
    registration_bonus = models.PositiveIntegerField()  # $

    def __str__(self):
        return self.institution
