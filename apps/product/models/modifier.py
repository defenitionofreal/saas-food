from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Modifier(models.Model):
    """
    Modifier of the product
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="modifiers",
        blank=True
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
