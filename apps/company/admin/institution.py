from django.contrib import admin
from apps.company.models import Institution, MinCartCost, Design


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ["id", "domain", "user"]
    search_fields = ("title",)


@admin.register(MinCartCost)
class MinCartCostAdmin(admin.ModelAdmin):
    search_fields = ("id",)

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ["id"]
    search_fields = ("id",)
