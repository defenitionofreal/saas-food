from django.db import models


class Design(models.Model):
    """
    Color of buttons and elements
    """
    institution = models.ManyToManyField("company.Institution",
                                         related_name="design")
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.institution}"
