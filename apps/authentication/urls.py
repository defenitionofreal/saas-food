from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from apps.authentication.api import auth_viewset
from apps.authentication.api.varify_email import EmailVerificationCodeView
from apps.authentication.api.confirm_email import EmailConfirmationCodeView
from apps.authentication.api.varify_phone import PhoneVerificationCodeView
from apps.authentication.api.confirm_phone import PhoneConfirmationCodeView

app_name = 'authentication'


router = routers.DefaultRouter()
router.register('', auth_viewset.AuthViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verification/email/', EmailVerificationCodeView.as_view()),
    path('confirmation/email/', EmailConfirmationCodeView.as_view()),
    path('verification/phone/', PhoneVerificationCodeView.as_view()),
    path('confirmation/phone/', PhoneConfirmationCodeView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view())  # refresh from cookie
    # todo: pass reset
]
