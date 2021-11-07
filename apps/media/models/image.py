from django.db import models


class Image(models.Model):
    """
    Image
    """
    title = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255, blank=True)
    picture = models.ImageField()

    def __str__(self):
        return self.title
