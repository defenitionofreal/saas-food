from django.urls import path
from apps.showcase.api.products_client_list import ProductsClientListAPIView
from apps.showcase.api.categories_client_list import CategoriesClientListAPIView
from apps.showcase.api.categories_client_detail import CategoriesClientDetailAPIView
from apps.showcase.api.banners_client_list import BannersClientListAPIView
from apps.showcase.api.banners_client_detail import BannersClientDetailAPIView

app_name = 'showcase'

urlpatterns = [
    path('products/', ProductsClientListAPIView.as_view()),
    path('categories/', CategoriesClientListAPIView.as_view()),
    path('categories/<str:slug>/', CategoriesClientDetailAPIView.as_view()),
    path('banners/', BannersClientListAPIView.as_view()),
    path('banners/<int:pk>/', BannersClientDetailAPIView.as_view()),
]
