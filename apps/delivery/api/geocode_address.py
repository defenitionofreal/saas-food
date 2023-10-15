from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission,
    OrganizationGeocoderTokenPermission, OrganizationInstitutionPermission
)
from apps.delivery.services.geocoder import KladrSuggestions

from apps.delivery.models import InstitutionAddress
from apps.delivery.serializers import InstitutionAddressSerializer


import os


class OrganizationYandexAddressGeocodeAPIView(APIView):

    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission,
                          OrganizationInstitutionPermission,
                          OrganizationGeocoderTokenPermission]
    http_method_names = ["post"]

    def post(self, request):
        institution_id = request.data.get("institution_id", None)
        query = request.data.get("query", None)
        user = self.request.user
        geocoder_token = user.yandexgeocodertoken_set.first()

        if not user.inst_user.filter(id=institution_id).exists():
            raise ValidationError({"detail": "Wrong institution id."})

        kladr = KladrSuggestions(os.environ.get("KLADR_API_KEY"))
        address_detail = kladr.address_detail(geocoder_token.api_key, query)

        address, _ = InstitutionAddress.objects.update_or_create(
            user_id=user.id,
            institution_id=institution_id,
            defaults=kladr.address_data_after_yandex_geocoder(address_detail)
        )

        serializer = InstitutionAddressSerializer(address, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
