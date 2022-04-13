from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Bonus, UserBonus

from decimal import Decimal


class AddBonusAPIView(APIView):
    """
    Customer can write off his bonuses
    from a total cart cost or total cost after promocode
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, domain):
        user = self.request.user
        institution = Institution.objects.get(domain=domain)
        bonus = get_object_or_404(Bonus, institution=institution)
        cart = Cart.objects.get(institution=institution, customer=user)
        bonus_input = round(int(self.request.query_params.get("bonus")))
        try:
            if cart.customer_bonus is None:
                if bonus.is_active is True:
                    user_bonus = UserBonus.objects.filter(
                        institution=institution, user=user).first()
                    if user_bonus:

                        if bonus_input > user_bonus.bonus:
                            return Response({"detail": "Not enough bonuses."})

                        if cart.promo_code is not None:
                            if bonus.is_promo_code is True:
                                total_cart = cart.get_total_cart_after_sale
                                sale = round((bonus.write_off / Decimal(
                                    '100')) * total_cart)
                            else:
                                return Response({
                                                    "detail": "Use bonuses with promocode is not allowed."})
                        else:
                            total_cart = cart.get_total_cart
                            sale = round((bonus.write_off / Decimal(
                                '100')) * total_cart)

                        if bonus_input > sale:
                            return Response({
                                                "detail": f"Write off no more than {bonus.write_off}% of total price. ({sale} bonuses)"})
                        cart.customer_bonus = bonus_input
                        cart.save()
                        user_bonus.bonus -= bonus_input
                        user_bonus.save()
                        return Response({
                                            "detail": f"{bonus_input} bonuses have been successfully redeemed"})
                    else:
                        return Response(
                            {"detail": "You dont have any bonuses yet."})
                else:
                    return Response(
                        {"detail": "Loyalty program is not active"})
            else:
                return Response({"detail": "Bonuses already applied."})
        except Exception as e:
            return Response({"detail": f"{e}"})
