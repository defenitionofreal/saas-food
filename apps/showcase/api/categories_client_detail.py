from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.company.models import Institution
from apps.product.models import Category
from apps.product.serializers import CategorySerializer


class CategoriesClientDetailAPIView(APIView):

    def get(self, request, domain, slug):
        institution = Institution.objects.get(domain=domain)
        query = get_object_or_404(Category.objects, institution=institution,
                                  slug=slug)
        serializer = CategorySerializer(query)
        return Response(serializer.data)
