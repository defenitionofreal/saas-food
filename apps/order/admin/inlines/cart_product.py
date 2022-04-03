from django.contrib import admin
from apps.order.models import CartProduct


class CartProductInline(admin.TabularInline):
    model = CartProduct
    autocomplete_fields = ("product", "modifiers", "additives")
    extra = 0
