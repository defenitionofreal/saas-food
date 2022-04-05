from django.urls import path
from apps.order.api import (cart_detail,
                            add_to_cart,
                            remove_from_cart,
                            add_promocode_to_cart,
                            add_customer_bonus_to_cart)

app_name = 'order'

urlpatterns = [
    # customer добавленно в пути из-за проблем аунтентификации
    path('customer/cart/', cart_detail.CartAPIView.as_view()),  # нужно ли cart определять по своему id ?
    path('customer/cart/add/', add_to_cart.AddToCartAPIView.as_view()),
    path('customer/cart/remove/<str:product_slug>/', remove_from_cart.RemoveFromCartAPIView.as_view()),
    # add promo code
    path('customer/cart/code/', add_promocode_to_cart.AddPromoCodeAPIView.as_view()),
    # write off bonuses
    path('customer/cart/bonus/', add_customer_bonus_to_cart.AddBonusAPIView.as_view()),
]
