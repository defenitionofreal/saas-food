from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import NutritionalValueSerializer
from apps.product.models import NutritionalValue
from apps.authentication.permissions import ConfirmedAccountPermission


class NutritionalValueViewSet(viewsets.ModelViewSet):
    queryset = NutritionalValue.objects.all()
    serializer_class = NutritionalValueSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(product__user=self.request.user)
