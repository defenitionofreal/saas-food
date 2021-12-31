from django.contrib import admin
from apps.delivery.models import DeliveryZoneFile


@admin.register(DeliveryZoneFile)
class DeliveryZoneFileAdmin(admin.ModelAdmin):
    search_fields = ("institution",)
    autocomplete_fields = ("institution",)