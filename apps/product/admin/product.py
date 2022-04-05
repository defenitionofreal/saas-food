from django.contrib import admin
from apps.product.models import Product
from django.db import models


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "is_active")
    list_filter = ("institution", "is_active")
    search_fields = ("title",)
    ordering = ("title", "pk")
    autocomplete_fields = ("institution", "category", "sticker", "images", "additives")

    actions = ("activate_products", "deactivate_products")

    @admin.action(description="Activate products")
    def activate_products(self, request, queryset):
        self._set_active(queryset, is_active=True)

    @admin.action(description="Deactivate products")
    def deactivate_products(self, request, queryset):
        self._set_active(queryset, is_active=False)

    def _set_active(self, queryset: models.QuerySet, is_active: bool) -> None:
        queryset.filter(is_active=not is_active).update(is_active=is_active)
