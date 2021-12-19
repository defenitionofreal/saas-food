from django.urls import path
from .api import (city_create,)

app_name = 'location'

urlpatterns = [
    path('new/', city_create.CityCreateAPIView.as_view()),
]
