from django.urls import path
from .api import (category_create,
                  category_list,
                  category_detail,
                  additive_create,
                  additive_list,
                  additive_detail,
                  sticker_create,
                  sticker_list,
                  sticker_detail,
                  product_create,
                  product_list,
                  product_detail,
                  modifier_create,
                  modifier_list,
                  modifier_detail,
                  modifier_price_create,
                  modifier_price_list,
                  modifier_price_detail)


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
   # product
   path('institution/<uuid:pk>/product/new/', product_create.ProductCreateAPIView.as_view()),
   path('institution/<uuid:pk>/product/list/', product_list.ProductListAPIView.as_view()),
   path('institution/<uuid:pk>/product/detail/<int:product_pk>/', product_detail.ProductDetailAPIView.as_view()),
   # modifier
   path('institution/<uuid:pk>/modifier/new/', modifier_create.ModifierCreateAPIView.as_view()),
   path('institution/<uuid:pk>/modifier/list/', modifier_list.ModifierListAPIView.as_view()),
   path('institution/<uuid:pk>/modifier/detail/<int:modifier_pk>/', modifier_detail.ModifierDetailAPIView.as_view()),
   # modifier price
   path('institution/<uuid:pk>/modifier/<int:modifier_pk>/price/new/', modifier_price_create.ModifierPriceCreateAPIView.as_view()),
   path('institution/<uuid:pk>/modifier/price/list/', modifier_price_list.ModifierPriceListAPIView.as_view()),
   path('institution/<uuid:pk>/modifier/<int:modifier_pk>/price/detail/<int:modifier_price_pk>/', modifier_price_detail.ModifierPriceDetailAPIView.as_view()),
]
