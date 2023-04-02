from django.db import models
from django.contrib.auth import get_user_model
import hashlib

User = get_user_model()

# TODO: hash api keys!
# Hashing function
def hash_api_key(api_key):
    return hashlib.sha256(api_key.encode()).hexdigest()

# Unhashing function
def unhash_api_key(hashed_api_key):
    return lambda candidate_api_key: hash_api_key(candidate_api_key) == hashed_api_key


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
