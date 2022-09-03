from rest_framework.views import APIView
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
        bonus_input = round(int(self.request.query_params.get("bonus")))
        cart = CartHelper(request, institution)
        return cart.add_bonuses(bonus_input)
