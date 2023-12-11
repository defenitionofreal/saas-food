from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.delivery.models import YandexGeocoderToken
from apps.delivery.serializers import YandexGeocoderTokenSerializer

from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission,
    OrganizationInstitutionPermission
)


class YandexGeocoderViewSet(viewsets.ModelViewSet):
    queryset = YandexGeocoderToken.objects.all()
    serializer_class = YandexGeocoderTokenSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission,
                          OrganizationInstitutionPermission]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

