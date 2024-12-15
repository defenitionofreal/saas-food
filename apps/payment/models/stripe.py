from django.db import models
from django.contrib.auth import get_user_model
from apps.base.models import SecureCharField

User = get_user_model()


class StripeIntegration(models.Model):
    """
    Model for organization stripe api key
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stripe_integration"
    )
    api_key = SecureCharField(unique=True)

    def __str__(self):
        return self.user.email
