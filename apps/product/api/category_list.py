from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Category
from apps.product.serializers import CategorySerializer
from apps.base.authentication import JWTAuthentication


class CategoryListAPIView(APIView):
    """ List Category """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Category.objects.filter(institution=institution)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)
