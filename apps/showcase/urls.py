from django.urls import path
from .api.test_products import Test

app_name = 'showcase'

urlpatterns = [
    path('', Test.as_view()),
]
