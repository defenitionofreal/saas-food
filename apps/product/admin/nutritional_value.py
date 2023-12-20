from django.contrib import admin
from apps.product.models import NutritionalValue


@admin.register(NutritionalValue)
class NutritionalValueAdmin(admin.ModelAdmin):
    ordering = ("id", )
    autocomplete_fields = ("product_id", "modifier_id")
    list_display = ("id", "product_id", "modifier_id", "protein", "fats",
                    "carbohydrates", "calories")
