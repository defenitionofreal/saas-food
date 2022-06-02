from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.location.models import AddressLink
from apps.location.serializers import AddressLinkSerializer


class AddressListAPIView(APIView):
    """ List Address's """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = AddressLink.objects.filter(user=self.request.user)
        serializer = AddressLinkSerializer(query, many=True)
        return Response(serializer.data)
