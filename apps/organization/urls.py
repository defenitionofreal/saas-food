from django.urls import path, include

# views from order app !
# promo codes (coupons)
from apps.order.api.promocode_create import PromoCodeCreateAPIView
from apps.order.api.promocode_list import PromoCodeListAPIView
from apps.order.api.promocode_detail import PromoCodeDetailAPIView
# bonus
from apps.order.api.bonus_update_or_create import BonusCreateAPIView
from apps.order.api.bonus_delete import BonusDetailAPIView


app_name = 'organization'

urlpatterns = [
    path('', include('apps.base.urls', namespace='base')),
    path('institution/', include('apps.company.urls', namespace='company')),
    path('', include('apps.delivery.urls', namespace='delivery')),
    path('', include('apps.product.urls', namespace='product')),
    # promo code
    path('institution/<uuid:pk>/promocode/new/', PromoCodeCreateAPIView.as_view()),
    path('institution/<uuid:pk>/promocode/list/', PromoCodeListAPIView.as_view()),
    path('institution/<uuid:pk>/promocode/detail/<int:promo_code_pk>/', PromoCodeDetailAPIView.as_view()),
    # bonus
    path('institution/<uuid:pk>/bonus/new/', BonusCreateAPIView.as_view()),
    path('institution/<uuid:pk>/bonus/detail/<int:bonus_pk>/', BonusDetailAPIView.as_view()),
]
