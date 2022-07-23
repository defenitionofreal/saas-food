from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.services.cart_helper import CartHelper


class AddBonusAPIView(APIView):
    """
    Customer can write off his bonuses
    from a total cart cost or total cost after promocode
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        cart_helper = CartHelper(request=request, institution=institution)
        q_bonus = self.request.query_params.get("bonus")
        try:
            bonus_input = round(int(q_bonus))
            return cart_helper.add_customer_bonus(bonus_input)
        except Exception as e:
            return Response({"detail": f"{e}"})
