from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Category
from apps.product.serializers import CategorySerializer


class CategoryListAPIView(APIView):
    """ List Category """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #institution = Institution.objects.filter(user=self.request.user)
        query = Category.objects.filter(user=self.request.user)
        serializer = CategorySerializer(query, many=True)
        return Response(serializer.data)
