from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import AdditiveSerializer
from apps.product.models import Additive
from apps.authentication.permissions import ConfirmedAccountPermission


class AdditiveViewSet(viewsets.ModelViewSet):
    queryset = Additive.objects.all()
    serializer_class = AdditiveSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
