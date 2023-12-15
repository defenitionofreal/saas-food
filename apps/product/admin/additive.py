from django.contrib import admin
from apps.product.models import Additive


@admin.register(Additive)
class AdditiveAdmin(admin.ModelAdmin):
    search_fields = ("id", "category", "title",)
    ordering = ("pk",)
    list_display = ("id", "user_id",  "category", "title", "price", "is_active")
    autocomplete_fields = ("user", "category", "institutions")
