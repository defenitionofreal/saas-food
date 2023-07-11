from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.order.serializers import PromoCodeSerializer
from apps.order.models import PromoCode
from apps.authentication.permissions import ConfirmedAccountPermission


class PromoCodeViewSet(viewsets.ModelViewSet):
    """
    View set for organization use only.
    """
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")
