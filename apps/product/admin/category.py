from django.contrib import admin
from apps.product.models import Category
from django.db import models


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "is_active")
    list_filter = ("institution", "is_active")
    search_fields = ("title",)
    ordering = ("title", "pk")

    actions = ("activate_categories", "deactivate_categories")

    @admin.action(description="Activate categories")
    def activate_categories(self, request, queryset):
        self._set_active(queryset, is_active=True)

    @admin.action(description="Deactivate categories")
    def deactivate_categories(self, request, queryset):
        self._set_active(queryset, is_active=False)

    def _set_active(self, queryset: models.QuerySet, is_active: bool) -> None:
        queryset.filter(is_active=not is_active).update(is_active=is_active)
