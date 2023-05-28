from django.urls import path, include
from .api import (
    category_viewset, additive_category_viewset, additive_viewset,
    sticker_viewset, product_viewset,

                  modifier_create,
                  modifier_list,
                  modifier_detail,
                  modifier_price_create,
                  modifier_price_list,
                  modifier_price_detail)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', category_viewset.CategoryViewSet, basename='categories')
router.register('additive-categories', additive_category_viewset.CategoryAdditiveViewSet, basename='additive_categories')
router.register('additives', additive_viewset.AdditiveViewSet, basename='additives')
router.register('stickers', sticker_viewset.StickerViewSet, basename='stickers')
router.register('products', product_viewset.ProductViewSet, basename='products')



app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),

    # TODO: NutritionalValues and Weight models!!! NEW
   # modifier
   path('modifier/new/', modifier_create.ModifierCreateAPIView.as_view()),
   path('modifier/list/', modifier_list.ModifierListAPIView.as_view()),
   path('modifier/detail/<int:modifier_pk>/', modifier_detail.ModifierDetailAPIView.as_view()),
   # modifier price
   path('modifier/<int:modifier_pk>/price/new/', modifier_price_create.ModifierPriceCreateAPIView.as_view()),
   path('modifier/price/list/', modifier_price_list.ModifierPriceListAPIView.as_view()),
   path('modifier/<int:modifier_pk>/price/detail/<int:modifier_price_pk>/', modifier_price_detail.ModifierPriceDetailAPIView.as_view()),
]
