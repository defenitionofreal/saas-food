from django.db import models

from apps.company.models.enums import WeekDay

#todo: remake weekday / timeinterval / deliveryInterval/ workTimeInterval at delivery app
class WorkingHours(models.Model):
    """
    Working time of institution
    """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ForeignKey(
        "company.Institution",
        on_delete=models.CASCADE,
        related_name="working_hours"
    )
    weekday = models.CharField(max_length=20, choices=WeekDay.choices)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return f"{self.institution}"
