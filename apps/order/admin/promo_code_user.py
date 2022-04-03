from django.contrib import admin

from apps.order.models import PromoCodeUser


@admin.register(PromoCodeUser)
class PromoCodeUserAdmin(admin.ModelAdmin):
    search_fields = ("id",)
