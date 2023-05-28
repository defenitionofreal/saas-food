from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.base.serializers import WeekDaySerializer
from apps.base.models import WeekDay
from apps.authentication.permissions import ConfirmedAccountPermission


class WeekDayViewSet(viewsets.ModelViewSet):
    queryset = WeekDay.objects.all()
    serializer_class = WeekDaySerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]
