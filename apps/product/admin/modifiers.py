from django.contrib import admin
from apps.product.models import Modifier, ModifierPrice


@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("pk", "title")
    list_display = ("id", "title")


@admin.register(ModifierPrice)
class ModifierPriceAdmin(admin.ModelAdmin):
    search_fields = ("modifier",)
    ordering = ("pk", "modifier")
    list_display = ("id", "modifier", "product", "price")
