from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import DesignSerializer
from apps.company.models import Design
from apps.authentication.permissions import ConfirmedAccountPermission


class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
