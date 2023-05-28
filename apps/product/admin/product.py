from django.contrib import admin
from apps.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("title", "pk")
    autocomplete_fields = ("institutions", "category", "stickers", "images",
                           "additives")
