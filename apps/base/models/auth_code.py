from django.db import models
from django.contrib.auth import get_user_model
from .managers import auth_code_manager

User = get_user_model()


class AuthCode(models.Model):
    """
    Authentication code for register and login customer by sms
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="auth_code")
    code = models.CharField(max_length=6, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = auth_code_manager.AuthCodeManager()

    def __str__(self):
        return f"{self.user}({self.code})"
