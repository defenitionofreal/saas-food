from django.contrib import admin
from apps.product.models import Sticker


@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    ordering = ("title", "pk")
