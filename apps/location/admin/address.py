from django.contrib import admin

from apps.location.models import Address, AddressLink


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass

@admin.register(AddressLink)
class AddressLinkAdmin(admin.ModelAdmin):
    pass

