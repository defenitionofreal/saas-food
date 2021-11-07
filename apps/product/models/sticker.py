from django.db import models


class Sticker(models.Model):
    """
    Sticker of product
    """
    institution = models.ForeignKey("apps.company.Institution", on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.title
