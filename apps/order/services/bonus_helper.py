from rest_framework import status
from rest_framework.response import Response
from apps.order.models.bonus import UserBonus, Bonus
from decimal import Decimal


# TODO: начислять бонусы если статус в заказе оплачен,
#  заберать обратно бонсы если статус в заказе отменен
#  подумать, можно ли начислять бонусы в заказе, если в заказе было списание бонусов!

class BonusHelper:
    def __init__(self, amount, cart, user):
        self.amount = amount
        self.cart = cart
        self.user = user
        self.bonus_rule = Bonus.objects.get(institutions=self.cart.institution)

    def _is_cart_has_bonuses(self):
        """
        if user didn't write off any bonuses yet check
        """
        if self.cart.customer_bonus is None:
            return True
        return Response({"detail": "Bonuses already applied."},
                        status=status.HTTP_400_BAD_REQUEST)

    def _is_company_bonus_rule_active(self):
        """
        Check if company set bonus rule and that rule is active
        """
        if self.bonus_rule and self.bonus_rule.is_active:
            return True
        return Response({"detail": "Loyalty program is not active"},
                        status=status.HTTP_400_BAD_REQUEST)

    def _get_user_bonuses(self):
        """
        Get user bonus balance
        """
        user_bonus, _ = UserBonus.objects.get_or_create(
            institution=self.cart.institution,
            user=self.user)
        return user_bonus

    def _is_customer_has_bonuses(self):
        """
        Check if customer bonuses amount bigger than 0
        """
        if self._get_user_bonuses().bonus > 0:
            return True
        return Response({"detail": "You dont have any bonuses yet."},
                        status=status.HTTP_400_BAD_REQUEST)

    def _is_input_amount_smaller_user_amount(self):
        """
        Check if input bonuses amount smaller than customer bonuses balance
        """
        if self._is_customer_has_bonuses():
            if self.amount <= self._get_user_bonuses().bonus:
                return True
            return Response({"detail": "Not enough bonuses."},
                            status=status.HTTP_400_BAD_REQUEST)

    def _is_use_bonuses_with_coupon(self):
        """
        Check if customer could use bonus write off together with coupon sale
        """
        if self.bonus_rule.is_promo_code is True:
            return True
        return False

    def _is_allowed_use_bonuses_with_apllied_coupon(self):
        if self.cart.promo_code is not None:
            if self._is_use_bonuses_with_coupon() is False:
                return Response(
                    {"detail": "Use bonuses with coupon is not allowed."},
                    status=status.HTTP_400_BAD_REQUEST)
        return True

    def max_write_off_amount(self):
        """
        Count max value that customer could write off from bonus balance
        """
        total_cart = self.cart.get_total_cart
        write_off_amount = 0
        if self.bonus_rule.is_active:
            if self.cart.promo_code is not None:
                if self._is_use_bonuses_with_coupon() is True:
                    write_off_amount = round((self.bonus_rule.write_off / Decimal("100")) * total_cart)
                # else false и нужно вернуть ошибку что нельзя с купоном бонусы списать
            else:
                write_off_amount = round((self.bonus_rule.write_off / Decimal("100")) * total_cart)
        return write_off_amount

    def _is_input_amount_smaller_write_off_amount(self):
        """
        Check if input amount smaller than amount that customer could write off
        """
        if self.amount <= self.max_write_off_amount():
            return True
        return Response(
            {"detail": f"Write off no more than {self.bonus_rule.write_off}% of total price. "
                       f"({self.max_write_off_amount()} bonuses)"},
            status=status.HTTP_400_BAD_REQUEST)

    def main(self):
        cart_has_bonuses = self._is_cart_has_bonuses()
        active_bonus_rule = self._is_company_bonus_rule_active()
        customer_has_bonuses = self._is_customer_has_bonuses()
        input_sm_user_bonuses = self._is_input_amount_smaller_user_amount()
        input_sm_write_off = self._is_input_amount_smaller_write_off_amount()
        bonus_with_applied_coupon = self._is_allowed_use_bonuses_with_apllied_coupon()

        rule_list = [active_bonus_rule,
                     cart_has_bonuses,
                     customer_has_bonuses,
                     bonus_with_applied_coupon,
                     input_sm_user_bonuses,
                     input_sm_write_off]

        for res in rule_list:
            if res is not True:
                return res

        self.cart.customer_bonus = self.amount
        self.cart.save()
        user_balance = self._get_user_bonuses()
        user_balance.bonus -= self.amount
        user_balance.save()

        return Response(
            {"detail": f"{self.amount} bonuses been successfully redeemed"},
            status=status.HTTP_201_CREATED)
