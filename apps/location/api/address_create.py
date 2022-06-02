from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.location.serializers import AddressSerializer
from apps.location.models import Address, AddressLink
from apps.company.models import Institution
from apps.company.services.compare_institution import (_find_wrong_inst_id,
                                                       _check_duplicated_uuid)


class AddressCreateAPIView(APIView):
    """ Create new address """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = self.request.user
        serializer = AddressSerializer(data=request.data)

        institution = Institution.objects.filter(user=user)
        address_link = AddressLink.objects.filter(user=user)
        data = request.data["institution"]

        if data:
            if _find_wrong_inst_id(data, institution.values_list('id',
                                                                 flat=True)):
                return Response({"detail": f"wrong institution id"},
                                status=status.HTTP_400_BAD_REQUEST)
            if _check_duplicated_uuid(data,
                                      address_link.values_list('institution',
                                                               flat=True)):
                return Response(
                    {"detail": f"institution already has an address"},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "institution is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()

            # create address link obj that connect user with a address
            affiliate = institution.filter(id=data[0])
            if affiliate.exists():
                AddressLink.objects.create(user=user,
                                           institution=affiliate.first(),
                                           address=Address.objects.filter(
                                               id=serializer.data[
                                                   "id"]).first())
            else:
                AddressLink.objects.create(user=user,
                                           address=Address.objects.filter(
                                               id=serializer.data[
                                                   "id"]).first())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
