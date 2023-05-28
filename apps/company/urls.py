from .api import (
    institution_viewset, design_viewset, analytics_viewset,
    social_links_viewset, requisites_viewset, banner_viewset,
    extra_phone_viewset, min_cart_cost_viewset, week_day_viewset,
    work_hours_viewset,
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
router.register('week-days', week_day_viewset.WeekDayViewSet, basename='week_days')
router.register('work-hours', work_hours_viewset.WorkHoursViewSet, basename='work_hours')




app_name = 'company'

urlpatterns = [
    path('', include(router.urls)),

    path('geocoding/', geocoding.GetAddressApiView.as_view()),
    path('dashboard/', dashboard.DashboardView.as_view()),  # temperary test request
    # TODO: LATER
    # orders
    # path('orders/list/', orders_list.OrderListAPIView.as_view()),
    # path('orders/detail/<uuid:order_pk>/', order_detail.OrderDetailAPIView.as_view()),
    # payments stuff
    # path('yoomoney/', set_yoomoney.YooMoneyCreateAPIView.as_view())

]
