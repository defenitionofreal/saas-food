from .api import (
    institution_viewset, design_viewset, analytics_viewset,
    social_links_viewset, requisites_viewset, banner_viewset,
    extra_phone_viewset, min_cart_cost_viewset,
                  working_hours_create,
                  working_hours_list,
                  working_hours_detail,
                  dashboard,
                  geocoding,
                  orders_list,
                  order_detail,
                  set_yoomoney)

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('institutions', institution_viewset.InstitutionViewSet, basename='institutions')
router.register('designs', design_viewset.DesignViewSet, basename='designs')
router.register('analytics', analytics_viewset.AnalyticsViewSet, basename='analytics')
router.register('social-links', social_links_viewset.SocialLinksViewSet, basename='social_links')
router.register('requisites', requisites_viewset.RequisitesViewSet, basename='requisites')
router.register('banners', banner_viewset.BannerViewSet, basename='banners')
router.register('extra-phones', extra_phone_viewset.ExtraPhoneViewSet, basename='extra_phones')
router.register('cart-cost', min_cart_cost_viewset.MinCartCostViewSet, basename='cart_cost')


app_name = 'company'

urlpatterns = [
    path('', include(router.urls)),

    path('geocoding/', geocoding.GetAddressApiView.as_view()),
    path('dashboard/', dashboard.DashboardView.as_view()),  # temperary test request
    # working hours
    # path('<uuid:pk>/working-hours/new/', working_hours_create.WorkingHoursCreateAPIView.as_view()),
    # path('<uuid:pk>/working-hours/list/', working_hours_list.WorkingHoursListAPIView.as_view()),
    # path('<uuid:pk>/working-hours/detail/<int:working_hours_pk>/', working_hours_detail.WorkingHoursDetailAPIView.as_view()),
    # TODO: LATER
    # orders
    # path('orders/list/', orders_list.OrderListAPIView.as_view()),
    # path('orders/detail/<uuid:order_pk>/', order_detail.OrderDetailAPIView.as_view()),
    # payments stuff
    # path('yoomoney/', set_yoomoney.YooMoneyCreateAPIView.as_view())

]
