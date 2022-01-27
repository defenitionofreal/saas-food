from django.contrib import admin
from apps.company.models import Institution, MinCartCost


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    autocomplete_fields = ("address",)


@admin.register(MinCartCost)
class MinCartCostAdmin(admin.ModelAdmin):
    search_fields = ("id",)
