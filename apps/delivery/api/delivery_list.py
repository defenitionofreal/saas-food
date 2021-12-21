from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.delivery.models import Delivery
from apps.delivery.serializers import DeliverySerializer
from apps.base.authentication import JWTAuthentication


class DeliveryListAPIView(APIView):
    """ List Delivery """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Delivery.objects.filter(institution=institution)
        serializer = DeliverySerializer(query, many=True)
        return Response(serializer.data)
