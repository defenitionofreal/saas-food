from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from apps.company.models import Institution
from apps.company.models import WorkHours
from apps.company.serializers import WorkHoursSerializer

from apps.showcase.serializers import OpenHoursSerializer

import pytz
import datetime


class WorkHoursViewSet(viewsets.ModelViewSet):
    queryset = WorkHours.objects.all()
    serializer_class = WorkHoursSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get"]

    def get_queryset(self):
        domain = self.kwargs['domain']
        institution = Institution.objects.get(domain=domain)
        qs = WorkHours.objects.filter(institutions=institution)
        return qs

    @action(detail=False, methods=["get"],
            url_path="check-open-hours",
            serializer_class=OpenHoursSerializer)
    def check_open_hours(self, request, *args, **kwargs):
        domain = kwargs['domain']
        institution = Institution.objects.get(domain=domain)
        institution_timezone = institution.organizationtimezone_set.first()

        if not institution_timezone:
            raise ValidationError({"detail": f"Timezone is not set at {institution.domain}"})

        now = datetime.datetime.now()
        timezone = pytz.timezone(institution_timezone.timezone)
        now_with_tz = timezone.localize(now)

        actual_day_of_week_number = now_with_tz.isoweekday()
        actual_time = now_with_tz.time()

        work_hours = self.get_queryset().filter(
            institutions=institution,
            weekdays__position=actual_day_of_week_number,
            from_hour__lte=actual_time,
            to_hour__gte=actual_time
        )
        is_open: bool = work_hours.exists()

        serializer = self.get_serializer({'is_open': is_open})
        return Response(serializer.data)
