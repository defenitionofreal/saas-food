from django.urls import path

from .api import session

app_name = 'base'

urlpatterns = [
    path('session/', session.SessionAPIView.as_view(), name='session'),
    # path('user/', user_view.UserAPIView.as_view()),
    # check payment status (yoomoney)
    # TODO: (yoomoney) убрать в более базовый урл без приставки auth
    # path('yoomoney-notification/', yoomoney_notification.YooMoneyHttpNotificationAPIView.as_view())
]


