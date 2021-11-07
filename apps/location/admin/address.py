from django.contrib import admin

from apps.location.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ("city__title", "region__title", "street__title")
    autocomplete_fields = ("city", "region", "street")
