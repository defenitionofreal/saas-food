from django.contrib import admin

from apps.order.models import Cart, CartItem, Order, OrderItem, PromoCode, \
    Bonus, PromoCodeUser, UserBonus


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id",]
    search_fields = ("id",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(PromoCodeUser)
class PromoCodeUserAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    #list_display = ['id']
    search_fields = ("id",)


@admin.register(UserBonus)
class UserBonusAdmin(admin.ModelAdmin):
    search_fields = ("id",)
