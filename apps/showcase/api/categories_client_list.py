from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.product.models import Category
from apps.product.serializers import CategorySerializer


class CategoriesClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Category.objects.filter(institution=institution,
                                       is_active=True).order_by('row')
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)
