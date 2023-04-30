from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OrganizationSmsProvider(models.Model):
    """
    Model for organization's SMS providers to store their API credentials.

    Institutions field if user (organization) want to use provider on specific
    affiliates.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User as organization"
    )
    institutions = models.ManyToManyField(
        "company.Institution",
        verbose_name="Could choose only specific affiliates or all"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Sms provider title"
    )
    api_login = models.CharField(
        max_length=500,
        verbose_name="API login, account id or any auth data"
    )
    api_key = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="API key, token or password"
    )
    api_additional = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Any API additional data if needed"
    )
    company_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Company title",
        help_text="Show company title as a message sender."
    )
    from_phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Sending message from that phone number",
        help_text="If company title is not possible to use."
    )
    is_active = models.BooleanField(
        default=True
    )
