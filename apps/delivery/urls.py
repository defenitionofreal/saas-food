from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.delivery.api import (
    suggestions, delivery_zone_viewset, institution_address_viewset,
    customer_address_viewset, delivery_type_rule_viewset
)


app_name = 'delivery'

router = DefaultRouter()
router.register('delivery/organization/type-rules', delivery_type_rule_viewset.DeliveryTypeRuleViewSet, basename='delivery-type-rule')
router.register('delivery/organization/zones', delivery_zone_viewset.OrganizationDeliveryZoneViewSet, basename='delivery-zone')
router.register('delivery/organization/address', institution_address_viewset.InstitutionAddressViewSet, basename='delivery-address')
router.register('delivery/customer/address', customer_address_viewset.CustomerAddressViewSet, basename='delivery-customer-zone')


organization_urlpatterns = [
    # path('delivery/organization-geocoder/', geocode_address.OrganizationYandexAddressGeocodeAPIView.as_view()),  # step 2
]

showcase_urlpatterns = [
    # delivery affiliate points
    # customer delivery address
    # set customer delivery address
]

urlpatterns = [
    path('', include(router.urls)),
    # suggestions to get right address string for a geocoder
    path('delivery/suggestions/', suggestions.KladrSuggestionsAPIView.as_view()),
]
