from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import Analytics
from apps.company.serializers import AnalyticsSerializer


class AnalyticsClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Analytics.objects.filter(institution=institution,
                                         is_active=True)
        serializer = AnalyticsSerializer(query, many=True)
        return Response(serializer.data)
