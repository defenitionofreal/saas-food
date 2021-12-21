from django.urls import path
from .api import (category_create,
                  category_list,
                  category_detail,
                  additive_create,
                  additive_list,
                  additive_detail,
                  sticker_create,
                  sticker_list,
                  sticker_detail)


app_name = 'product'

urlpatterns = [
   # for dashboard

   # category
   path('institution/<uuid:pk>/category/new/', category_create.CategoryCreateAPIView.as_view()),
   path('institution/<uuid:pk>/category/list/', category_list.CategoryListAPIView.as_view()),
   path('institution/<uuid:pk>/category/detail/<int:category_pk>/', category_detail.CategoryDetailAPIView.as_view()),
   # additive
   path('institution/<uuid:pk>/additive/new/', additive_create.AdditiveCreateAPIView.as_view()),
   path('institution/<uuid:pk>/additive/list/', additive_list.AdditiveListAPIView.as_view()),
   path('institution/<uuid:pk>/additive/detail/<int:additive_pk>/', additive_detail.AdditiveDetailAPIView.as_view()),
   # sticker
   path('institution/<uuid:pk>/sticker/new/', sticker_create.StickerCreateAPIView.as_view()),
   path('institution/<uuid:pk>/sticker/list/', sticker_list.StickerListAPIView.as_view()),
   path('institution/<uuid:pk>/sticker/detail/<int:sticker_pk>/', sticker_detail.StickerDetailAPIView.as_view()),
]