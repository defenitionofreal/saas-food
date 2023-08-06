from rest_framework.exceptions import ValidationError
from apps.order.models.bonus import UserBonus, Bonus


class BonusHelper:
    def __init__(self, amount, cart, user):
        self.amount = amount
        self.cart = cart
        self.user = user
        self.bonus_rule = Bonus.objects.filter(
            institutions=self.cart.institution, is_active=True
        ).first()

    def _validate_cart_has_no_customer_bonus(self):
        """
        if user didn't write off any bonuses yet check
        """
        if self.cart.customer_bonus:
            raise ValidationError({"detail": "Bonuses already applied."})

    def _validate_company_bonus_rule(self):
        """
        Check if company set bonus rule and that rule is active
        """
        if not self.bonus_rule:
            raise ValidationError({"detail": "Bonus rule not found"})

    def _get_user_bonuses(self) -> UserBonus:
        """
        Get user bonus balance
        """
        user_bonus, _ = UserBonus.objects.get_or_create(
            institution_id=self.cart.institution.id,
            user_id=self.user.id
        )
        return user_bonus

    def _validate_customer_has_bonuses(self):
        """
        Check if customer bonuses amount bigger than 0
        """
        user_bonus_balance = self._get_user_bonuses()
        if user_bonus_balance.bonus == 0:
            raise ValidationError({"detail": "You dont have any bonuses yet."})

    def _validate_input_amount_smaller_user_bonus_balance(self):
        """
        Check if input bonuses amount smaller than customer bonuses balance
        """
        user_bonus_balance = self._get_user_bonuses()
        if self.amount > user_bonus_balance.bonus:
            raise ValidationError({"detail": "Not enough bonuses."})

    def _validate_use_bonuses_with_applied_coupon(self):
        if self.cart.promo_code and not self.bonus_rule.is_promo_code:
            raise ValidationError({"detail": "Use bonuses with coupon is not allowed."})

    def _validate_input_amount_smaller_write_off_amount(self):
        """
        Check if input amount smaller than amount that customer could write off
        """
        if self.amount > self.cart.get_bonus_write_off:
            raise ValidationError(
                {"detail": f"Write off no more than {self.bonus_rule.write_off}% of total price. "
                           f"({self.cart.get_bonus_write_off} bonuses)"}
            )

    def main(self):
        self._validate_cart_has_no_customer_bonus()
        self._validate_company_bonus_rule()
        self._validate_customer_has_bonuses()
        self._validate_input_amount_smaller_user_bonus_balance()
        self._validate_input_amount_smaller_write_off_amount()
        self._validate_use_bonuses_with_applied_coupon()

        self.cart.customer_bonus = self.amount
        self.cart.save()

        # TODO: начислять бонусы если статус в заказе оплачен,
        #  забирать обратно бонусы если статус в заказе отменен

        user_balance = self._get_user_bonuses()
        user_balance.bonus -= self.amount
        user_balance.save()
