from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import WeightSerializer
from apps.product.models import Weight
from apps.authentication.permissions import ConfirmedAccountPermission


class WeightViewSet(viewsets.ModelViewSet):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(product__user=self.request.user)
