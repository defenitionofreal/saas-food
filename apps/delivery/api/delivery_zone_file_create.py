from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.delivery.serializers import DeliveryZoneFileSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import Institution

from apps.delivery.tasks import google_map_file_upload_task

from django.conf import settings
import os

class DeliveryZoneFileCreateAPIView(APIView):
    """ Create new delivery zone file """
    parser_classes = (parsers.MultiPartParser,)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = DeliveryZoneFileSerializer(data=request.data)
        institution = Institution.objects.get(pk=pk)
        if serializer.is_valid():
            try:
                serializer.save(institution=institution)
                google_map_file_upload_task.delay(serializer.data['file'],
                                                  str(institution.id))
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                raise {'Error': e}
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
