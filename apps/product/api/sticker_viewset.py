from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import StickerSerializer
from apps.product.models import Sticker
from apps.authentication.permissions import ConfirmedAccountPermission


class StickerViewSet(viewsets.ModelViewSet):
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
