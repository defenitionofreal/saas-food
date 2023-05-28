from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Sticker(models.Model):
    """
    Sticker of product
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="stickers",
        blank=True
    )
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    color = models.CharField(max_length=20)
    text_color = models.CharField(max_length=20, default="#000")

    def __str__(self):
        return self.title
