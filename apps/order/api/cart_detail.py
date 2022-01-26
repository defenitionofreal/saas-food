from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution, MinCartCost
from apps.order.models import Cart
from apps.order.serializers import CartSerializer
from apps.base.authentication import JWTAuthentication


class CartAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        try:
            cart = Cart.objects.get(institution=institution, customer=user)

            cart_cost = MinCartCost.objects.filter(institution=institution).first()
            if cart_cost:
                cart.min_amount = cart_cost.cost

            if cart.items.exists():
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            else:
                return Response({"detail": "Cart is empty."})
        except Exception as e:
            return Response({"detail": f"Cart does not exist. {e}"})
