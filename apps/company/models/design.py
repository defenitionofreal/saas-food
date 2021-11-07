from django.db import models


class Design(models.Model):
    """
    Color of buttons and elements
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="design")
    color = models.CharField(max_length=100)  # возможно использовать пакет для api colorfield?

    def __str__(self):
        return f"{self.institution}"
