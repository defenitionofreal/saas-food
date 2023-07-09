from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import ModifierSerializer
from apps.product.models import Modifier
from apps.authentication.permissions import ConfirmedAccountPermission


class ModifierViewSet(viewsets.ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
