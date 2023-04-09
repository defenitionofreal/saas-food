from django.urls import path, include
from rest_framework import routers

from apps.customer.views import CheckCustomerView
from apps.customer.api import customer_viewset

app_name = 'customer'


router = routers.DefaultRouter()
router.register('dashboard', customer_viewset.CustomerViewSet)

urlpatterns = [
    path('check/', CheckCustomerView.as_view()),
    path('', include(router.urls)),
]
