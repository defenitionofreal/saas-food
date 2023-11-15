from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.delivery.api import (suggestions, delivery_zone_viewset)


app_name = 'delivery'

router = DefaultRouter()
router.register('delivery/zones', delivery_zone_viewset.OrganizationDeliveryZoneViewSet, basename='delivery-zone')

urlpatterns = [
    path('', include(router.urls)),
    # suggestions to get right address string for a geocoder
    path('delivery/suggestions/', suggestions.KladrSuggestionsAPIView.as_view()),
    # organization views
    # path('delivery/organization-geocoder/', geocode_address.OrganizationYandexAddressGeocodeAPIView.as_view()),  # step 2

    # # delivery zones
    # todo продумать как и где в дашборде будет раздел настрйоки доставки и в итоге как реаоизовать api
    # path('delivery-zone/new/', delivery_zone_create.DeliveryZoneCreateAPIView.as_view()),
    # # delivery zones file (stopped for a while!)
    # path('institution/<uuid:pk>/delivery-zone/file/new/', delivery_zone_file_create.DeliveryZoneFileCreateAPIView.as_view()),
]
