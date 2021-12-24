from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Product
from apps.product.serializers import ProductSerializer



class Test(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Product.objects.filter(institution=institution)
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)
