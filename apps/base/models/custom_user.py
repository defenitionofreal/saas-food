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
    # permission flags
    is_customer = models.BooleanField(default=False)
    is_promo = models.BooleanField(default=False)  # for free promos
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)  # sms code check ?

    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = user_manager.UserManager()

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Name: {self.last_name} {self.first_name} {self.middle_name},"
            f"Phone: {str(self.phone)}, Email: {self.email}"
        )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        # убрать unique=True у email и username и сделать unique_together ??
        # unique_together = ["phone", "email", "username"]

        constraints = [
            # проверить ограничение
            models.CheckConstraint(
                check=models.Q(
                    phone__isnull=False) | models.Q(email__isnull=False),
                name="User must have one of the fields: phone, email"),
            # # условия
            # models.UniqueConstraint(
            #     fields=["phone"],
            #     condition=models.Q(phone__isnull=False),
            #     name="Unique phone numbers for users",
            # ),
            # models.UniqueConstraint(
            #     fields=["email"],
            #     condition=models.Q(email__isnull=False),
            #     name="Unique emails for users",
            # ),
            # models.UniqueConstraint(
            #     fields=["username"],
            #     condition=models.Q(username__isnull=False),
            #     name="Unique usernames for users",
            # ),
        ]
