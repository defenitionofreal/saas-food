from django.urls import path, include
from rest_framework import routers

from apps.authentication.api import auth_viewset

app_name = 'authentication'


router = routers.DefaultRouter()
router.register('', auth_viewset.AuthViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
