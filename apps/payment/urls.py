from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.payment.api.finish import FinishPaymentAPIView
from apps.payment.api.stripe import StripeWebHookAPIView
from apps.payment.api import paymnet_viewset

# 61234817-85c4-45c3-ab1b-22b3db7996d3
app_name = 'payment'

router = DefaultRouter()
router.register('payment/organization', paymnet_viewset.PaymentTypeInstitutionViewSet, basename='payment')

# TODO: (yoomoney) пока беспонтовая вьюшка
urlpatterns = [
    path('', include(router.urls)),

    path("success/", FinishPaymentAPIView.as_view()),
    path("stripe/<str:domain>/", StripeWebHookAPIView.as_view())
]
