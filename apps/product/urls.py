from django.urls import path, include
from .api import (
    category_viewset, additive_category_viewset, additive_viewset,
    sticker_viewset, product_viewset, modifier_viewset,

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
router.register('modifiers', modifier_viewset.ModifierViewSet, basename='modifiers')




app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),

    # TODO: Also NutritionalValues and Weight models!!! NEW
   # modifier price
   path('modifier/<int:modifier_pk>/price/new/', modifier_price_create.ModifierPriceCreateAPIView.as_view()),
   path('modifier/price/list/', modifier_price_list.ModifierPriceListAPIView.as_view()),
   path('modifier/<int:modifier_pk>/price/detail/<int:modifier_price_pk>/', modifier_price_detail.ModifierPriceDetailAPIView.as_view()),
]
