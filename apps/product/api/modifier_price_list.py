from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import ModifierPrice
from apps.product.serializers import ModifierPriceSerializer
from apps.base.authentication import JWTAuthentication


class ModifierPriceListAPIView(APIView):
    """ List modifiers prices """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = ModifierPrice.objects.filter(institution=institution)
        serializer = ModifierPriceSerializer(query, many=True)
        return Response(serializer.data)
