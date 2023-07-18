from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import ExtraPhone
from apps.company.serializers import ExtraPhoneSerializer


class ExtraPhoneClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = ExtraPhone.objects.filter(institutions=institution)
        serializer = ExtraPhoneSerializer(query, many=True)
        return Response(serializer.data)
