from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.company.serializers import AnalyticsSerializer
from apps.company.models import Analytics
from apps.authentication.permissions import ConfirmedAccountPermission


class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.all()
    serializer_class = AnalyticsSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]
