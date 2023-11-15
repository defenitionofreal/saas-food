from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.delivery.serializers import DeliveryZoneSerializer
from apps.delivery.models import DeliveryZone
from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission,
    OrganizationGeocoderTokenPermission, OrganizationInstitutionPermission
)


class OrganizationDeliveryZoneViewSet(viewsets.ModelViewSet):
    queryset = DeliveryZone.objects.all()
    serializer_class = DeliveryZoneSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission,
                          OrganizationInstitutionPermission,
                          OrganizationGeocoderTokenPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
