from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.product.serializers import ProductSerializer
from apps.base.authentication import JWTAuthentication
from apps.product.models import Product


class ProductDetailAPIView(APIView):
    """
    Retrieve, update or delete a product.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, product_pk):
        query = get_object_or_404(Product.objects, institution_id=pk, pk=product_pk)
        serializer = ProductSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, product_pk):
        query = get_object_or_404(Product.objects, institution_id=pk, pk=product_pk)
        serializer = ProductSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, product_pk):
        query = get_object_or_404(Product.objects, institution_id=pk, pk=product_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
