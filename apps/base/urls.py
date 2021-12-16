from django.urls import path

from . import views
from .api import (user_view,
                  register_view,
                  login_view,
                  logout_view)

from rest_framework import routers

app_name = 'base'

router = routers.DefaultRouter()

#router.register(r'api/v1/user', user_view.UserViewSet, basename='user')

urlpatterns = [
    path('', views.index, name='index'),
    path('register', register_view.RegisterAPIView.as_view()),
    path('login', login_view.LoginAPIView.as_view()),
    path('logout', logout_view.LogoutAPIView.as_view()),
    path('user', user_view.UserAPIView.as_view())
]

urlpatterns += router.urls
