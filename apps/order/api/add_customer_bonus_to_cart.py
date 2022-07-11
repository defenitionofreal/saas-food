from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Bonus, UserBonus


class AddBonusAPIView(APIView):
    """
    Customer can write off his bonuses
    from a total cart cost or total cost after promo code
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, domain):
        user = self.request.user
        institution = Institution.objects.get(domain=domain)
        bonus = get_object_or_404(Bonus, institution=institution)
        cart = Cart.objects.get(institution=institution, customer=user)
        bonus_input = round(int(self.request.query_params.get("bonus")))
        try:
            if cart.customer_bonus is not None:
                return Response({"detail": "Bonuses already applied."})

            if bonus.is_active is False:
                return Response({"detail": "Loyalty program is not active"})

            user_bonus:UserBonus = UserBonus.objects.filter(institution=institution, user=user).first()
            if not user_bonus:
                return Response({"detail": "You dont have any bonuses yet."})

            user_bonus_count = user_bonus.bonus
            if bonus_input > user_bonus_count:
                return Response({"detail": "Not enough bonuses."})

            is_used_bonus_with_promo_code = cart.promo_code is not None and bonus.is_promo_code is False
            if is_used_bonus_with_promo_code:
                return Response({"detail": "Use bonuses with promocode is not allowed."})

            total_cart = cart.get_total_cart_after_sale
            bonus_write_off = bonus.write_off
            sale = bonus.get_write_off_absolute_amount(total_cart)

            if bonus_input > sale:
                r = {"detail": f"Write off no more than {bonus_write_off}% of total price. ({sale} bonuses)"}
                return Response(r)

            cart.set_customer_bonus_amount(bonus_input)
            user_bonus.write_off_bonus_amount(bonus_input)

            return Response({"detail": f"{bonus_input} bonuses have been successfully redeemed"})

        except Exception as e:
            return Response({"detail": f"{e}"})
