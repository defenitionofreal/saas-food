from django.db import models


class VerificationCode(models.Model):
    """
    Verify code for email or phone
    """
    code = models.CharField(
        max_length=4
    )
    email = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    is_confirmed = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ('-created_at',)
