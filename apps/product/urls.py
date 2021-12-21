from django.urls import path
from .api import (category_create,
                  category_list,
                  category_detail)


app_name = 'product'

urlpatterns = [
   # for dashboard
   path('institution/<uuid:pk>/category/new/', category_create.CategoryCreateAPIView.as_view()),
   path('institution/<uuid:pk>/category/list/', category_list.CategoryListAPIView.as_view()),
   path('institution/<uuid:pk>/category/detail/<int:category_pk>/', category_detail.CategoryDetailAPIView.as_view()),
]