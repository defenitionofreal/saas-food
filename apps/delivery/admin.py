from django.contrib import admin
from apps.delivery.models import DeliveryZoneFile, DeliveryZone, DeliveryZoneСoordinates


@admin.register(DeliveryZoneFile)
class DeliveryZoneFileAdmin(admin.ModelAdmin):
    search_fields = ("institution",)
    autocomplete_fields = ("institution",)

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    search_fields = ("institution",)
    autocomplete_fields = ("institution",)

@admin.register(DeliveryZoneСoordinates)
class DeliveryZoneСoordinatesAdmin(admin.ModelAdmin):
    search_fields = ("zone",)
    autocomplete_fields = ("zone",)