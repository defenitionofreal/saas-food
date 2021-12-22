from django.contrib import admin
from apps.product.models import Modifier, ModifierPrice


@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("title", "pk")


@admin.register(ModifierPrice)
class ModifierPriceAdmin(admin.ModelAdmin):
    search_fields = ("modifier",)
    ordering = ("modifier", "pk")
