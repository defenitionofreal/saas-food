from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.order.api import (
                            select_payment_type,
                            checkout,
                            cart_viewset)

app_name = 'order'


router = DefaultRouter()
router.register('', cart_viewset.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),

    # todo: lets refactor this all shit
    # # select payment type
    # path('customer/cart/payment/type/', select_payment_type.SelectPaymentTypeAPIView.as_view()),
    # # checkout
    # path('customer/checkout/', checkout.CheckoutAPIView.as_view())
]
