from django.urls import path
from .api import (address_create,)

app_name = 'location'

urlpatterns = [
    path('address/new/', address_create.AddressCreateAPIView.as_view()),
]
