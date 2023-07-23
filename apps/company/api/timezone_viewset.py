from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.cache import cache
from django.conf import settings

from apps.company.serializers import (
    OrganizationTimeZoneSerializer, TimeZoneListSerializer
)
from apps.company.models import OrganizationTimeZone
from apps.authentication.permissions import ConfirmedAccountPermission

import pytz


class OrganizationTimeZoneViewSet(viewsets.ModelViewSet):
    queryset = OrganizationTimeZone.objects.all()
    serializer_class = OrganizationTimeZoneSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["get"],
            serializer_class=TimeZoneListSerializer)
    def all(self, request):
        cache_key = 'all_timezones_cache'
        all_timezones = cache.get(cache_key)

        if not all_timezones:
            all_timezones = [tz for tz in pytz.all_timezones]
            cache.set(cache_key, all_timezones, settings.CACHE_TTL)

        serializer = TimeZoneListSerializer({"timezone": all_timezones})
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def local(self, request):
        # todo: экшен для передачи локального часового пояса автоматически!
        pass
