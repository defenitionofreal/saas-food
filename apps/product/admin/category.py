from django.contrib import admin
from apps.product.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("title", "pk")
