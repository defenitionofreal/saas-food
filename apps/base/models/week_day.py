from django.db import models


class WeekDay(models.Model):
    title = models.CharField(max_length=50)
    position = models.SmallIntegerField()

    def __str__(self):
        return self.title
