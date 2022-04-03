from django.contrib import admin

from apps.order.models import CartProduct


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    autocomplete_fields = ("product", "modifiers", "additives")
