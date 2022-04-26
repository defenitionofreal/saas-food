from django.urls import path, include
from .views import CheckCustomerView

app_name = 'customer'

urlpatterns = [
    path('check/', CheckCustomerView.as_view())
]
