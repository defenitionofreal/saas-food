from django.contrib import admin
from apps.delivery.models import (DeliveryZoneFile,
                                  DeliveryZone,
                                  DeliveryZoneСoordinates,
                                  Delivery)


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


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    search_fields = ("delivery_type",)
    autocomplete_fields = ("institution",)