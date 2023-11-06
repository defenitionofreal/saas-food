from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


from apps.company.serializers import InstitutionSerializer
from apps.company.models import Institution
from apps.delivery.models import InstitutionAddress

from apps.delivery.serializers import InstitutionAddressSerializer


from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission,
    OrganizationInstitutionPermission, OrganizationGeocoderTokenPermission
)
from apps.delivery.services.geocoder import KladrSuggestions

import os


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True,
            methods=["post"],
            url_path="address/create",
            serializer_class=InstitutionAddressSerializer,
            permission_classes=[IsAuthenticated,
                                ConfirmedAccountPermission,
                                OrganizationPermission,
                                OrganizationInstitutionPermission,
                                OrganizationGeocoderTokenPermission]
            )
    def create_address(self, request, pk):
        institution = get_object_or_404(
            Institution, user_id=self.request.user.id, pk=pk
        )
        query = request.data.get("query", "")
        user = self.request.user
        geocoder_token = user.yandexgeocodertoken_set.first()

        kladr = KladrSuggestions(os.environ.get("KLADR_API_KEY"))
        address_detail = kladr.address_detail(geocoder_token.api_key, query)

        address, _ = InstitutionAddress.objects.update_or_create(
            user_id=user.id,
            institution_id=institution.id,
            defaults=kladr.address_data_after_yandex_geocoder(address_detail)
        )
        serializer = InstitutionAddressSerializer(address, read_only=True)
        return Response(serializer.data)

    @action(detail=True,
            methods=["get", "delete"],
            serializer_class=InstitutionAddressSerializer
            )
    def address(self, request, pk):
        institution = get_object_or_404(
            Institution, user_id=self.request.user.id, pk=pk
        )
        address = institution.institutionaddress_set.all()
        if request.method == "DELETE":
            address.delete()
        serializer = InstitutionAddressSerializer(address, many=True)
        return Response(serializer.data)
