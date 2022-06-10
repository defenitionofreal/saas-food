from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.delivery.models import Delivery
from apps.delivery.serializers import DeliverySerializer


class DeliveryListAPIView(APIView):
    """ List Delivery """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Delivery.objects.filter(user=self.request.user)
        serializer = DeliverySerializer(query, many=True)
        return Response(serializer.data)
