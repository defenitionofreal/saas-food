from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Modifier
from apps.product.serializers import ModifierSerializer


class ModifierListAPIView(APIView):
    """ List modifiers """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Modifier.objects.filter(institution=institution)
        serializer = ModifierSerializer(query, many=True)
        return Response(serializer.data)
