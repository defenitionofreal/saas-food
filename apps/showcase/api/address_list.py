from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.location.models import AddressLink
from apps.location.serializers import AddressLinkSerializer


class AddressListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.only("id", "domain").get(
            domain=domain)
        query = AddressLink.objects.get(institution=institution)
        serializer = AddressLinkSerializer(query, many=False)
        return Response(serializer.data)
