from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.location.serializers import AddressLinkSerializer
from apps.location.models import AddressLink
from apps.company.models import Institution


class AddressDetailAPIView(APIView):
    """ Get affiliate (institution) address """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = self.request.user
        institution = Institution.objects.filter(id=pk)
        if institution.exists():
            address = AddressLink.objects.filter(user=user,
                                                 institution=institution[0])
            serializer = AddressLinkSerializer(address[0], many=False)
            return Response(serializer.data)
        return Response({"detail": "institution does not exist"},
                        status=status.HTTP_400_BAD_REQUEST)
