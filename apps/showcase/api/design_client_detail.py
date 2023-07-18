from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import Design
from apps.company.serializers import DesignSerializer


class DesignClientDetailAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        design = Design.objects.filter(institutions=institution).first()
        if not design:
            return Response({"detail": "no design"})
        serializer = DesignSerializer(design)
        return Response(serializer.data)
