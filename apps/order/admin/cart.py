from django.contrib import admin

from apps.order.admin.inlines import CartProductInline
from apps.order.models import Cart
from apps.order.services import CartService


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    inlines = (CartProductInline,)
    autocomplete_fields = ("institution", "customer", "promo_code")
    list_display = ("id", "total_coast")

    actions = ("calculate_cart_coast",)

    @admin.action(description="Calculate cart coast")
    def calculate_cart_coast(self, request, queryset):
        cart_service = CartService()
        for cart in queryset:
            cart_service.calculate_cart_coast(cart)
