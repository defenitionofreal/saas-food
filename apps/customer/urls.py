from django.urls import path, include
from .views import CheckCustomerView

app_name = 'customer'

urlpatterns = [
    path('', include('apps.base.urls', namespace='base')),
    path('check/', CheckCustomerView.as_view())
]
