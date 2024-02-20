from django.urls import path, include

# views from order app !
from apps.order.api.promocode_viewset import PromoCodeViewSet
from apps.order.api.bonus_viewset import BonusViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('promo-code', PromoCodeViewSet, basename='promo-code')
# router.register('bonus', BonusViewSet, basename='bonus')


app_name = 'organization'

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('apps.company.urls', namespace='company')),
    # path('', include('apps.delivery.urls', namespace='delivery')),
    # path('', include('apps.product.urls', namespace='product')),
    # path('', include('apps.payment.urls', namespace='payment')),
]