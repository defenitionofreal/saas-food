from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.conf import settings

from apps.company.models import Institution
from apps.delivery.models import InstitutionAddress

from apps.delivery.serializers import InstitutionAddressSerializer


from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission,
    OrganizationInstitutionPermission, OrganizationGeocoderTokenPermission
)
from apps.delivery.services.geocoder import KladrSuggestions

import os


class InstitutionAddressViewSet(viewsets.ModelViewSet):
    queryset = InstitutionAddress.objects.all()
    serializer_class = InstitutionAddressSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission,
                          OrganizationInstitutionPermission,
                          OrganizationGeocoderTokenPermission]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def create(self, request,*args, **kwargs):
        pk = request.data.get("institution_id", None)
        query = request.data.get("query", None)

        institution = get_object_or_404(
            Institution, user_id=self.request.user.id, pk=pk
        )
        user = self.request.user
        geocoder_token = user.yandexgeocodertoken_set.first()

        kladr = KladrSuggestions(settings.KLADR_API_KEY)
        address_detail = kladr.address_detail(geocoder_token.api_key, query)

        address, _ = InstitutionAddress.objects.update_or_create(
            user_id=user.id,
            institution_id=institution.id,
            defaults=kladr.address_data_after_yandex_geocoder(address_detail)
        )
        serializer = InstitutionAddressSerializer(address, read_only=True)
        return Response(serializer.data)
