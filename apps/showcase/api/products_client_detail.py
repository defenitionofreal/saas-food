from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.company.models import Institution
from apps.product.models import Product
from apps.product.serializers import ProductSerializer


class ProductClientDetailAPIView(APIView):

    def get(self, request, domain, slug):
        try:
            institution = Institution.objects.get(domain=domain)
        except Exception as e:
            return Response({"detail": f"{e}"})
        query = get_object_or_404(Product.objects, institution=institution,
                                  slug=slug)
        serializer = ProductSerializer(query)
        return Response(serializer.data)
