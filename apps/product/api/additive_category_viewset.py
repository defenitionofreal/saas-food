from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import CategoryAdditiveSerializer
from apps.product.models import CategoryAdditive
from apps.authentication.permissions import ConfirmedAccountPermission


class CategoryAdditiveViewSet(viewsets.ModelViewSet):
    queryset = CategoryAdditive.objects.all()
    serializer_class = CategoryAdditiveSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
