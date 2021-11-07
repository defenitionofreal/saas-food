from django.db import models

from company.models.enums import WeekDay


class WorkingHours(models.Model):
    """
    Working time of institution
    """
    institution = models.ForeignKey("apps.company.Institution", on_delete=models.CASCADE, related_name="working_hours")
    weekday = models.CharField(max_length=20, choices=WeekDay.choices)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return f"{self.institution}"
