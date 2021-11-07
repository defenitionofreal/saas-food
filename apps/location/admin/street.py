from django.contrib import admin

from location.models import Street


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    search_fields = ("title",)
