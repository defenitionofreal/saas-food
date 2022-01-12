from django.contrib import admin
from apps.product.models import CategoryAdditive


@admin.register(CategoryAdditive)
class CategoryAdditiveAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("title", "pk")
