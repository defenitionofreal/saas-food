from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import WorkHoursSerializer
from apps.company.models import WorkHours
from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission
)


class WorkHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkHours.objects.all()
    serializer_class = WorkHoursSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["request"] = self.request
    #     return context
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)
