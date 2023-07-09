from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import ModifierPriceSerializer
from apps.product.models import ModifierPrice
from apps.authentication.permissions import ConfirmedAccountPermission


class ModifierPriceViewSet(viewsets.ModelViewSet):
    queryset = ModifierPrice.objects.all()
    serializer_class = ModifierPriceSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(modifier__user=self.request.user)
