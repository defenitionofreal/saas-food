from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class StripeIntegration(models.Model):
    """
    Model for organisation stripe api key
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stripe_integration"
    )
    api_key = models.CharField(
        max_length=1000,
        verbose_name="Stripe secret key"
    )

    def __str__(self):
        return self.user.email
