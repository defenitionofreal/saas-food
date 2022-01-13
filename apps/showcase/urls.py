from django.urls import path
from .api.products_client_list import ProductsClientListAPIView
from .api.categories_client_list import CategoriesClientListAPIView
from .api.categories_client_detail import CategoriesClientDetailAPIView

app_name = 'showcase'

urlpatterns = [
    path('products/', ProductsClientListAPIView.as_view()),
    path('categories/', CategoriesClientListAPIView.as_view()),
    path('categories/<str:slug>/', CategoriesClientDetailAPIView.as_view()),

]
