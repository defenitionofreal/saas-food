from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.order.models import OrderItem
from apps.order.serializers import CartItemSerializer


class CartAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = OrderItem.objects.all()#filter(institution=institution)
        serializer = CartItemSerializer(query, many=True)
        return Response(serializer.data)