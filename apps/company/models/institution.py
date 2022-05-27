from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model

from apps.base.models.seo import SeoModel
from apps.base.models.address import AddressModel

from apps.company.models.enums.timezone_ru import RussianTimezone
from apps.company.services.path_qr_code import get_path_qr_code
from apps.company.services.path_logo import get_path_logo

from phonenumber_field.modelfields import PhoneNumberField

import uuid

User = get_user_model()


class Institution(SeoModel):
    """
    Institution(company) model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="inst_user")
    logo = models.ImageField(upload_to=get_path_logo,
                             validators=[FileExtensionValidator(
                                allowed_extensions=['jpg', 'jpeg', 'png'])],
                             blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    phone = PhoneNumberField()
    other_phone = models.ManyToManyField('company.ExtraPhone', blank=True,
                                         related_name="inst_other_phone")
    domain = models.CharField(max_length=255, unique=True)
    local_time = models.CharField(max_length=20,
                                  choices=RussianTimezone.choices,
                                  default=RussianTimezone.MOSCOW)
    qrcode = models.ImageField(upload_to=get_path_qr_code, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.qrcode:
            from apps.company.tasks import generate_qrcode_task
            generate_qrcode_task.delay(self.id)
        super().save(*args, **kwargs)
