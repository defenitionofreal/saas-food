from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.serializers import DesignSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import Design, Institution


class DesignListAPIView(APIView):
    """ Create new institution """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        design = Design.objects.filter(institution=institution)
        serializer = DesignSerializer(design, many=True)
        return Response(serializer.data)
