from django.db import models


class WorkHours(models.Model):
    """
    Working time of institution
    """
    user = models.ForeignKey(
        "base.CustomUser",
        on_delete=models.CASCADE
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="work_hours"
    )
    title = models.CharField(
        max_length=255,
        help_text="Work hours for 'Pizza Uno' at weekend."
    )
    weekdays = models.ManyToManyField(
        "base.WeekDay"
    )
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return f"{self.title}"
