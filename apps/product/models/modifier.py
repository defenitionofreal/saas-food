from django.db import models


class Modifier(models.Model):
    """
    Modifier of the product
    """
    institution = models.ForeignKey("company.Institution",
                                    on_delete=models.CASCADE,
                                    related_name="modifiers")
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
