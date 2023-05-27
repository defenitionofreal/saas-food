from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import ExtraPhoneSerializer
from apps.company.models import ExtraPhone
from apps.authentication.permissions import ConfirmedAccountPermission


class ExtraPhoneViewSet(viewsets.ModelViewSet):
    queryset = ExtraPhone.objects.all()
    serializer_class = ExtraPhoneSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
