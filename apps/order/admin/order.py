from django.contrib import admin

from apps.order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ("id",)
