from django.urls import path
from apps.payment.api.finish import FinishPaymentAPIView
from apps.payment.api.stripe import StripeWebHookAPIView

# 61234817-85c4-45c3-ab1b-22b3db7996d3
app_name = 'payment'
# TODO: (yoomoney) пока беспонтовая вьюшка
urlpatterns = [
    path("success/", FinishPaymentAPIView.as_view()),
    path("stripe/<str:domain>/", StripeWebHookAPIView.as_view())
]
