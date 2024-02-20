from django.urls import path, include
from .api import (
    category_viewset, additive_category_viewset, additive_viewset,
    sticker_viewset, product_viewset, modifier_viewset, modifier_price_viewset,
    modifier_weight_viewset, modifier_nutrition_viewset
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('organization/categories', category_viewset.CategoryViewSet, basename='categories')
router.register('organization/additive-categories', additive_category_viewset.CategoryAdditiveViewSet, basename='additive_categories')
router.register('organization/additives', additive_viewset.AdditiveViewSet, basename='additives')
router.register('organization/stickers', sticker_viewset.StickerViewSet, basename='stickers')
router.register('organization/products', product_viewset.ProductViewSet, basename='products')
router.register('organization/modifiers', modifier_viewset.ModifierViewSet, basename='modifiers')
# unique for a product modifier
router.register('organization/modifiers-price', modifier_price_viewset.ModifierPriceViewSet, basename='modifiers-price')
router.register('organization/weight', modifier_weight_viewset.WeightViewSet, basename='weight')
router.register('organization/nutrition', modifier_nutrition_viewset.NutritionalValueViewSet, basename='nutrition')


app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]
