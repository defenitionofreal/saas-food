from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.delivery.serializers import DeliveryZoneSerializer


class DeliveryZoneListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.only("id", "domain").get(
            domain=domain)
        zones = institution.dz.all()
        serializer = DeliveryZoneSerializer(zones, many=True)
        return Response(serializer.data)

