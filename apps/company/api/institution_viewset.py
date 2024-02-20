from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.company.serializers import InstitutionSerializer
from apps.company.models import Institution
from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission
)


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
