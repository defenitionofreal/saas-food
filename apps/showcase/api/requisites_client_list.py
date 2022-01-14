from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import Requisites
from apps.company.serializers import RequisitesSerializer


class RequisitesClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Requisites.objects.filter(institution=institution)
        serializer = RequisitesSerializer(query, many=True)
        return Response(serializer.data)
