from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.company.serializers import InstitutionSerializer
from apps.base.authentication import JWTAuthentication


class InstitutionListAPIView(APIView):
    """ Create new institution """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        snippets = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(snippets, many=True)
        return Response(serializer.data)
