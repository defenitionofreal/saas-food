from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.order.api import (
                            add_customer_bonus_to_cart,
                            select_payment_type,
                            checkout,
                            cart_viewset)

app_name = 'order'


router = DefaultRouter()
router.register('', cart_viewset.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),

    # todo: lets refactor this all shit
    # # write off bonuses
    # path('customer/cart/bonus/', add_customer_bonus_to_cart.AddBonusAPIView.as_view()),
    # # select payment type
    # path('customer/cart/payment/type/', select_payment_type.SelectPaymentTypeAPIView.as_view()),
    # # checkout
    # path('customer/checkout/', checkout.CheckoutAPIView.as_view())
]
