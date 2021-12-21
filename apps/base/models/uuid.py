from django.db import models
from uuid import uuid4
import random


class UUIDBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class PublicIDBase(models.Model):
    public_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )

    def generate_random_id(self, prefix, length):
        random_part = ''.join(
            random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for i in range(length - len(prefix))
        )
        return prefix + random_part

    class Meta:
        abstract = True
