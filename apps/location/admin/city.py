from django.contrib import admin

from apps.location.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ("title",)
