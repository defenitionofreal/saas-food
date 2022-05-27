from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.delivery.models import Delivery
from apps.delivery.serializers import DeliverySerializer


class DeliveryClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Delivery.objects.filter(institution=institution,
                                        is_active=True)
        serializer = DeliverySerializer(query, many=True)
        return Response(serializer.data)
