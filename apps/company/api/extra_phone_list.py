from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import ExtraPhone, Institution
from apps.company.serializers import ExtraPhoneSerializer
from apps.base.authentication import JWTAuthentication


class ExtraPhoneListAPIView(APIView):
    """ List phones """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = ExtraPhone.objects.filter(institution=institution)
        serializer = ExtraPhoneSerializer(query, many=True)
        return Response(serializer.data)
