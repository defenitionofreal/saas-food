from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.location.serializers import AddressSerializer
from apps.location.models import Address, AddressLink
from apps.company.models import Institution


class GetAddressAPIView(APIView):
    """ Get affiliate (institution) address """
    #permission_classes = [IsAuthenticated]

    def post(self, request):

        user = self.request.user
        serializer = AddressSerializer(data=request.data)

        institution = Institution.objects.filter(user=user)
        address_link = AddressLink.objects.filter(user=user)
        data = request.data["institution"]

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
