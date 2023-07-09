from django.urls import path, include
from .api import (
    category_viewset, additive_category_viewset, additive_viewset,
    sticker_viewset, product_viewset, modifier_viewset, modifier_price_viewset,
    modifier_weight_viewset, modifier_nutrition_viewset
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', category_viewset.CategoryViewSet, basename='categories')
router.register('additive-categories', additive_category_viewset.CategoryAdditiveViewSet, basename='additive_categories')
router.register('additives', additive_viewset.AdditiveViewSet, basename='additives')
router.register('stickers', sticker_viewset.StickerViewSet, basename='stickers')
router.register('products', product_viewset.ProductViewSet, basename='products')
router.register('modifiers', modifier_viewset.ModifierViewSet, basename='modifiers')
# unique for a product modifier
router.register('modifiers-price', modifier_price_viewset.ModifierPriceViewSet, basename='modifiers-price')
router.register('weight', modifier_weight_viewset.WeightViewSet, basename='weight')
router.register('nutrition', modifier_nutrition_viewset.NutritionalValueViewSet, basename='nutrition')


app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]
