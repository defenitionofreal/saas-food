from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import RequisitesSerializer
from apps.company.models import Requisites
from apps.authentication.permissions import ConfirmedAccountPermission


class RequisitesViewSet(viewsets.ModelViewSet):
    queryset = Requisites.objects.all()
    serializer_class = RequisitesSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
