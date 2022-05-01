from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.company.serializers import InstitutionSerializer


class InstitutionListAPIView(APIView):
    """ Create new institution """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        institution = Institution.objects.filter(user=self.request.user)
        serializer = InstitutionSerializer(institution,
                                           many=True,
                                           context={"request": request})
        return Response(serializer.data)
