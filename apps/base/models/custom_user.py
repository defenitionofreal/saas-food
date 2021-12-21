import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("User must have a phone")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            phone=self.phone
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_superuser = False
        user.is_customer = False
        user.is_promo = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have a phone")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_customer = False
        user.is_promo = False
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """ Custom User Model """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='images/users/', blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_promo = models.BooleanField(default=False)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'  # админ должен входить через почту а юзеры через моб
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email or self.phone or '-----'} [{self.id}]"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
