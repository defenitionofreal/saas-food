from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.order.api import (promocode_viewset,
                            bonus_viewset,
                            select_payment_type,
                            checkout,
                            cart_viewset)

app_name = 'order'


router = DefaultRouter()
router.register('organization/promo-code', promocode_viewset.PromoCodeViewSet, basename='promo-code')
router.register('organization/bonus', bonus_viewset.BonusViewSet, basename='bonus')
router.register('customer', cart_viewset.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    # todo: lets refactor this all shit
    # # select payment type
    # path('customer/cart/payment/type/', select_payment_type.SelectPaymentTypeAPIView.as_view()),
    # # checkout
    # path('customer/checkout/', checkout.CheckoutAPIView.as_view())
]
