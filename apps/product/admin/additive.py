from django.contrib import admin
from apps.product.models import Additive


@admin.register(Additive)
class AdditiveAdmin(admin.ModelAdmin):
    search_fields = ("id", "title",)
    ordering = ("pk",)
    list_display = ("id", "title")
