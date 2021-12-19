from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import WorkingHours, Institution
from apps.company.serializers import WorkingHoursSerializer
from apps.base.authentication import JWTAuthentication


class WorkingHoursListAPIView(APIView):
    """ List working hours """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = WorkingHours.objects.filter(institution=institution)
        serializer = WorkingHoursSerializer(query, many=True)
        return Response(serializer.data)
