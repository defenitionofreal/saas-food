from django.contrib import admin
from apps.company.models import (
    Institution, MinCartCost, Design, ExtraPhone, WorkHours,
    OrganizationTimeZone
)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ["id", "domain", "user"]
    search_fields = ("title",)
    autocomplete_fields = ("user",)


@admin.register(MinCartCost)
class MinCartCostAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    autocomplete_fields = ("user", "institutions")


@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ("id",)
    autocomplete_fields = ("user", "institutions")


@admin.register(ExtraPhone)
class ExtraPhoneAdmin(admin.ModelAdmin):
    list_display = ["id", "phone", "position"]
    search_fields = ("id",)
    autocomplete_fields = ("user", "institutions")


@admin.register(WorkHours)
class WorkHoursAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ("id",)
    autocomplete_fields = ("user",)


@admin.register(OrganizationTimeZone)
class OrganizationTimeZoneAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "timezone"]
    search_fields = ("id",)
    autocomplete_fields = ("user", )
