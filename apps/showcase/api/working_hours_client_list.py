from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import WorkHours
from apps.company.serializers import WorkHoursSerializer


class WorkHoursClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = WorkHours.objects.filter(institutions=institution)
        serializer = WorkHoursSerializer(query, many=True)
        return Response(serializer.data)
