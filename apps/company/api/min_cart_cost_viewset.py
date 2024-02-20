from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import MinCartCostSerializer
from apps.company.models import MinCartCost
from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission
)


class MinCartCostViewSet(viewsets.ModelViewSet):
    queryset = MinCartCost.objects.all()
    serializer_class = MinCartCostSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
