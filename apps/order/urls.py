from django.urls import path
from apps.order.api.cart_detail import CartAPIView
from apps.order.api.add_to_cart import AddToCartAPIView
from apps.order.api.remove_from_cart import RemoveFromCartAPIView
from apps.order.api.add_promocode_to_cart import AddPromoCodeAPIView

app_name = 'order'

urlpatterns = [
    # customer добавленно в пути из-за проблем аунтентификации
    path('customer/cart/', CartAPIView.as_view()),  # нужно ли cart определять по своему id ?
    path('customer/cart/add/<str:product_slug>/', AddToCartAPIView.as_view()),
    path('customer/cart/remove/<str:product_slug>/', RemoveFromCartAPIView.as_view()),
    # promo code
    path('customer/cart/code/', AddPromoCodeAPIView.as_view()),
]
