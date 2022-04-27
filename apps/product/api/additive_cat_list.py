from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.product.models import CategoryAdditive
from apps.product.serializers import CategoryAdditiveSerializer


class CategoryAdditiveListAPIView(APIView):
    """ List Additive Categories"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = CategoryAdditive.objects.filter(user=self.request.user)
        serializer = CategoryAdditiveSerializer(query, many=True)
        return Response(serializer.data)
