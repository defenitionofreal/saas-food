from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.order.serializers import BonusSerializer
from apps.order.models import Bonus
from apps.authentication.permissions import ConfirmedAccountPermission


class BonusViewSet(viewsets.ModelViewSet):
    """
    View set for organization use only.
    """
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")
