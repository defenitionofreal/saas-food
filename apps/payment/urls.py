from django.urls import path
from apps.payment.api.finish import FinishPaymentAPIView


app_name = 'payment'
# TODO: (yoomoney) пока беспонтовая вьюшка
urlpatterns = [
    path("success/", FinishPaymentAPIView.as_view()),
]
