from django.urls import path
from .api import (address_create,
                  address_list,
                  address_detail)

app_name = 'location'

urlpatterns = [
    path('address/new/', address_create.AddressCreateAPIView.as_view()),
    path('address/list/', address_list.AddressListAPIView.as_view()),
    path('institution/<uuid:pk>/address/detail/', address_detail.AddressDetailAPIView.as_view()),
]
