from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import CategoryAdditive
from apps.product.serializers import CategoryAdditiveSerializer
from apps.base.authentication import JWTAuthentication


class CategoryAdditiveListAPIView(APIView):
    """ List Additive Categories"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = CategoryAdditive.objects.filter(institution=institution)
        serializer = CategoryAdditiveSerializer(query, many=True)
        return Response(serializer.data)
