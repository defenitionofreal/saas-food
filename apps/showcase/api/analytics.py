from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import Analytics
from apps.company.serializers import AnalyticsSerializer


class AnalyticsAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = get_object_or_404(
            Analytics, institution=institution, is_active=True
        )
        serializer = AnalyticsSerializer(query)
        return Response(serializer.data)
