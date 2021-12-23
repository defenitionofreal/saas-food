from django.db import models
from django.contrib.auth import get_user_model
from apps.company.models.analytics import Analytics

User = get_user_model()


class Plan(models.Model):
    """
    Pricing plan model
    """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_institutions = models.PositiveIntegerField(default=0)
    max_banners = models.PositiveIntegerField(default=0)
    max_analytics = models.ManyToManyField(Analytics)
    is_delivery_zone = models.BooleanField(default=False)
    is_live_queue = models.BooleanField(default=False)
    is_design = models.BooleanField(default=False)
    is_notifications = models.BooleanField(default=False)
    is_integrations = models.BooleanField(default=False)  #IIKO и так далее или может manytomany сделать?
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

