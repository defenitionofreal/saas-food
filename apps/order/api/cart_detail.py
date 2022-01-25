from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
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
            if cart.items.exists():
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            else:
                return Response({"detail": "Cart is empty."})
        except Exception as e:
            return Response({"detail": f"Cart does not exist. {e}"})
