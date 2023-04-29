from django.db import models
from apps.base.models.enums import LogTypes, LogStatus


class MessageLog(models.Model):
    type = models.CharField(max_length=3, choices=LogTypes.choices)
    status = models.CharField(max_length=3,
                              choices=LogStatus.choices,
                              default=None)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_type(self):
        choice = next((c[1] for c in LogTypes.choices if c[0] == int(self.type)), None)
        return choice if choice else ""

    @property
    def get_status(self):
        choice = next((c[1] for c in LogStatus.choices if c[0] == int(self.status)), None)
        return choice if choice else ""
