from django.contrib import admin

from apps.order.models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ("id",)
