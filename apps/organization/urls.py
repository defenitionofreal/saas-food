from django.urls import path, include

# views from order app !
from apps.order.api.promocode_viewset import PromoCodeViewSet
# bonus
from apps.order.api.bonus_update_or_create import BonusCreateAPIView
from apps.order.api.bonus_delete import BonusDetailAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('promo-code', PromoCodeViewSet, basename='promo-code')


app_name = 'organization'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('apps.company.urls', namespace='company')),
    path('', include('apps.delivery.urls', namespace='delivery')),
    path('', include('apps.product.urls', namespace='product')),
    path('', include('apps.location.urls', namespace='location')),
    # bonus
    path('institution/<uuid:pk>/bonus/new/', BonusCreateAPIView.as_view()),
    path('institution/<uuid:pk>/bonus/detail/<int:bonus_pk>/', BonusDetailAPIView.as_view()),
]

# TODO: написать вьюсеты на правила промокода и бонуса еще, потом можно двигаться к действиям покупателя или модулю доставки!
