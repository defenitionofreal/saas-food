from django.db import models


class Street(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
