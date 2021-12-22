from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.base.authentication import JWTAuthentication


class ProductListAPIView(APIView):
    """ List products """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Product.objects.filter(institution=institution)
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)
