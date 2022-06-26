from django.urls import path

from . import views
from .api import (user_view,
                  register_view,
                  login_view,
                  logout_view,
                  login_by_code,
                  send_auth_code,

                  yoomoney_notification)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'base'


urlpatterns = [
    path('', views.index, name='index'),

    # organization
    path('register/', register_view.RegisterAPIView.as_view()),
    path('login/', login_view.LoginOrganizationTokenView.as_view()),
    # customer
    path('reset-code/', send_auth_code.SendAuthCodeView.as_view()),
    path('login/phone/', login_by_code.AuthCustomerAPIView.as_view()),

    path('token/refresh/', TokenRefreshView.as_view()),

    # при jwt токенах логаут нету,
    # планируется удалять токены на фронт-енде
    # ну или дописать logout и заносить токены в blacklist
    path('logout', logout_view.LogoutAPIView.as_view()),

    # TODO: дописать get/put на прифили пользователей для смены паролей и т.д.
    path('user/', user_view.UserAPIView.as_view()),

    # check payment status (yoomoney)
    # TODO: (yoomoney) убрать в более базовый урл без приставки auth
    path('yoomoney-notification/', yoomoney_notification.YooMoneyHttpNotificationAPIView.as_view())
]


