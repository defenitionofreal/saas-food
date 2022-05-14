from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.product.models import Product
from apps.product.serializers import ProductListSerializer

from django.db.models import Prefetch


class ProductsClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.filter(domain=domain).only("id",
                                                                     "domain")

        query = Product.objects.filter(is_active=True,
                                       institution=institution.first())\
            .prefetch_related(Prefetch("institution", institution),
                              "images", "sticker")\
            .only("id", "category", "row", "title", "slug",
                  "price", "old_price", "images", "sticker").order_by('row')

        serializer = ProductListSerializer(query, many=True)
        return Response(serializer.data)
