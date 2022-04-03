from django.contrib import admin

from apps.order.models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    ordering = ("title", "pk")
