from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.company.models import Institution
from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ProductClientDetailAPIView(APIView):

    def get(self, request, domain, pk):
        institution = Institution.objects.get(domain=domain)
        query = get_object_or_404(Product.objects, institution=institution,
                                  pk=pk)
        serializer = ProductSerializer(query)
        return Response(serializer.data)
