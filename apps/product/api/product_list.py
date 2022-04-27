from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ProductListAPIView(APIView):
    """ List products """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Product.objects.filter(user=self.request.user)
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)
