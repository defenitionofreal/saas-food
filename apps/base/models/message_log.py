from django.db import models
from apps.base.models.enums import LogTypes, LogStatus


class MessageLog(models.Model):
    type = models.CharField(max_length=3, choices=LogTypes.choices)
    status = models.CharField(max_length=3,
                              choices=LogStatus.choices,
                              default=None)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
