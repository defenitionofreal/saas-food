from django.db import models
import pytz


class OrganizationTimeZone(models.Model):
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        blank=True,
        help_text="if no institutions then timezone is for all."
    )
    timezone = models.CharField(
        max_length=255,
        choices=[(tz, tz) for tz in pytz.all_timezones],
    )

    def __str__(self):
        return f"{self.id} - {self.timezone}"
