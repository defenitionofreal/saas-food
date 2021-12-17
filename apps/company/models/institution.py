from django.db import models
from apps.base.models.seo import SeoModel
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

import uuid

User = get_user_model()


class Institution(SeoModel):
    """
    Institution(company) model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="institutions")
    logo = models.ImageField(upload_to='images/users/', blank=True)  # images/users/self.user/institution/
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    phone = PhoneNumberField()  # возможность добавить доп номер еще
    domain = models.CharField(max_length=255, unique=True)
    address = models.ForeignKey("location.Address", on_delete=models.SET_NULL, null=True, related_name="+")
    local_time = models.CharField(max_length=255)  # через что должно быть поле выбора местного времени, список?

    def __str__(self):
        return self.title
