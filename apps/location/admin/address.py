from django.contrib import admin

from apps.location.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

