from django.contrib import admin
from apps.product.models import Weight


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    ordering = ("id", "weight_unit")
    autocomplete_fields = ("product_id", "modifier_id")
    list_display = ("id", "product_id", "modifier_id", "weight_unit", "weight")
