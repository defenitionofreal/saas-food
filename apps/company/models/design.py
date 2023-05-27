from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Design(models.Model):
    """
    Color of buttons and elements
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    institutions = models.ManyToManyField(
        "company.Institution",
        related_name="design"
    )
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}"
