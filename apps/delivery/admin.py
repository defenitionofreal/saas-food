from django.contrib import admin
from apps.delivery.models import (
    DeliveryZone, CartDeliveryInfo, CustomerAddress, InstitutionAddress,
    YandexGeocoderToken
)


@admin.register(YandexGeocoderToken)
class YandexGeocoderTokenAdmin(admin.ModelAdmin):
    list_display = ("user",)
    autocomplete_fields = ("user",)


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active")
    autocomplete_fields = ("institutions",)



@admin.register(CartDeliveryInfo)
class CartDeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "type")
    autocomplete_fields = ("cart",)



@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    autocomplete_fields = ("user",)



@admin.register(InstitutionAddress)
class InstitutionAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "institution")
    autocomplete_fields = ("user", "institution",)
