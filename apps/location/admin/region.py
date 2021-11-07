from django.contrib import admin

from location.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ("title",)
