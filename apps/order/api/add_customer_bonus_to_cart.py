from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.company.models import Institution
from apps.order.models import Cart, CartItem, Bonus, UserBonus

from apps.base.authentication import JWTAuthentication
import datetime


class AddBonusAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain):
        today = datetime.datetime.now().date()
        user = self.request.user
        bonus_amount = self.request.query_params.get("bonus")
        bonus = get_object_or_404(Bonus, user=user)
        institution = Institution.objects.get(domain=domain)
        cart = Cart.objects.get(institution=institution, customer=user)

        try:
            pass
        except Exception as e:
            return Response({"detail": f"{e}"})