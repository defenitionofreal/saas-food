from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.order.serializers import CartHelperSerializer


class CartAPIView(APIView):
    """
    Detailed information about current cart
    """

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        cart_serializer = CartHelperSerializer(request=request, institution=institution, context={"request": request})
        if cart_serializer.is_empty:
            return Response({"detail": "Cart is empty."})
        return Response(cart_serializer.data)
