from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import BannerSerializer
from apps.company.models import Banner
from apps.authentication.permissions import ConfirmedAccountPermission


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
