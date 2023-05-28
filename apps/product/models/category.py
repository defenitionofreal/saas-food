from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Category of institution
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="categories",
        blank=True
    )
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    row = models.PositiveIntegerField(default=1)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
