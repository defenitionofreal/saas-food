from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.order.models import OrderItem, CartItem, Cart
from apps.order.serializers import CartSerializer
from apps.base.authentication import JWTAuthentication


class CartAPIView(APIView):

    authentication_classes = [JWTAuthentication]

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        print(user)
        query = Cart.objects.get(institution=institution, customer=user)
        print(query)
        serializer = CartSerializer(query)
        return Response(serializer.data)
