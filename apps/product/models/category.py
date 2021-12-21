from django.db import models


class Category(models.Model):
    """
    Category of institution
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    row = models.PositiveIntegerField(default=1)
    slug = models.SlugField()

    def __str__(self):
        return self.title
