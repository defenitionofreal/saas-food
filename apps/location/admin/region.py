from django.contrib import admin

from apps.location.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ("title",)
