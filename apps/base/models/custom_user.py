from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from django.core.validators import FileExtensionValidator

from apps.base.services.path_profile_img import get_path_profile
from .managers import user_manager
import uuid


class CustomUser(AbstractUser):
    """ Custom User Model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # contact info
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255, blank=True,
                                null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    # name info
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    # profile image
    image = models.ImageField(upload_to=get_path_profile,
                              blank=True, null=True,
                              validators=[FileExtensionValidator(
                                  allowed_extensions=['jpg', 'jpeg', 'png'])])
    password = models.CharField(max_length=255)
    # permission flags
    is_customer = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    is_free_promo = models.BooleanField(default=False)
    is_sms_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  # todo: phone or email?
    REQUIRED_FIELDS = []

    objects = user_manager.UserManager()

    def __str__(self):
        value = str(self.id)
        if self.phone:
            value = str(self.phone)
        if not self.phone and self.email:
            value = str(self.email)
        return value

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        constraints = [
            # проверить ограничение
            models.CheckConstraint(
                check=models.Q(
                    phone__isnull=False) | models.Q(email__isnull=False),
                name="User must have one of the fields: phone, email"
            )
        ]
