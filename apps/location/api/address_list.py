from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.location.models import Address, AddressLink
from apps.location.serializers import AddressSerializer, AddressLinkSerializer


class AddressListAPIView(APIView):
    """ List Address's """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = AddressLink.objects.filter(user=self.request.user)
        # address_ids = query.select_related("address").values_list("address_id",
        #                                                           flat=True)
        # address = Address.objects.filter(id__in=address_ids)
        # serializer = AddressSerializer(address, many=True)
        serializer = AddressLinkSerializer(query, many=True)
        return Response(serializer.data)
