from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.product.models import Modifier
from apps.product.serializers import ModifierSerializer


class ModifierListAPIView(APIView):
    """ List modifiers """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Modifier.objects.filter(user=self.request.user)
        serializer = ModifierSerializer(query, many=True)
        return Response(serializer.data)
