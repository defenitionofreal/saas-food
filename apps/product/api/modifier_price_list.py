from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.product.models import ModifierPrice
from apps.product.serializers import ModifierPriceSerializer


class ModifierPriceListAPIView(APIView):
    """ List modifiers prices """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = ModifierPrice.objects.filter(user=self.request.user)
        serializer = ModifierPriceSerializer(query, many=True)
        return Response(serializer.data)
