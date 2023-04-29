from django.urls import path, include
from rest_framework import routers

from apps.authentication.api import auth_viewset
from apps.authentication.api.varify_email import EmailVerificationCodeView
from apps.authentication.api.confirm_email import EmailConfirmationCodeView
from apps.authentication.api.varify_phone import PhoneVerificationCodeView

app_name = 'authentication'


router = routers.DefaultRouter()
router.register('', auth_viewset.AuthViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verification/email/', EmailVerificationCodeView.as_view()),
    path('confirmation/email/', EmailConfirmationCodeView.as_view()),
    path('verification/phone/', PhoneVerificationCodeView.as_view())
]
