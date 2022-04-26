from django.urls import path
from .api import (institution_create,
                  institution_list,
                  institution_detail,
                  design_create,
                  design_detail,
                  analytics_create,
                  analytics_detail,
                  socials_create,
                  socials_detail,
                  requisites_create,
                  requisites_detail,
                  working_hours_create,
                  working_hours_list,
                  working_hours_detail,
                  extra_phone_create,
                  extra_phone_list,
                  extra_phone_detail,
                  banner_create,
                  banner_list,
                  banner_detail,
                  min_cart_cost_update_create,
                  min_cart_cost_delete,
                  dashboard)

app_name = 'company'

urlpatterns = [
    path('dashboard/', dashboard.DashboardView.as_view()),
    # institution
    path('new/', institution_create.InstitutionCreateAPIView.as_view()),
    path('list/', institution_list.InstitutionListAPIView.as_view()),
    path('<uuid:pk>/', institution_detail.InstitutionDetailAPIView.as_view()),
    # design
    path('design/new/', design_create.DesignCreateAPIView.as_view()),
    path('<uuid:pk>/design/detail/<int:design_pk>/', design_detail.DesignDetailAPIView.as_view()),
    # analytics
    path('<uuid:pk>/analytics/new/', analytics_create.AnalyticsCreateAPIView.as_view()),
    path('<uuid:pk>/analytics/detail/<int:analytics_pk>/', analytics_detail.AnalyticsDetailAPIView.as_view()),
    # social links
    path('<uuid:pk>/social-links/new/', socials_create.SocialsCreateAPIView.as_view()),
    path('<uuid:pk>/social-links/detail/<int:socials_pk>/', socials_detail.SocialsDetailAPIView.as_view()),
    # requisites
    path('<uuid:pk>/requisites/new/', requisites_create.RequisitesCreateAPIView.as_view()),
    path('<uuid:pk>/requisites/detail/<int:requisites_pk>/', requisites_detail.RequisitesDetailAPIView.as_view()),
    # working hours
    path('<uuid:pk>/working-hours/new/', working_hours_create.WorkingHoursCreateAPIView.as_view()),
    path('<uuid:pk>/working-hours/list/', working_hours_list.WorkingHoursListAPIView.as_view()),
    path('<uuid:pk>/working-hours/detail/<int:working_hours_pk>/', working_hours_detail.WorkingHoursDetailAPIView.as_view()),
    # extra phones
    path('<uuid:pk>/extra-phones/new/', extra_phone_create.ExtraPhoneCreateAPIView.as_view()),
    path('<uuid:pk>/extra-phones/list/', extra_phone_list.ExtraPhoneListAPIView.as_view()),
    path('<uuid:pk>/extra-phones/detail/<int:extra_phones_pk>/', extra_phone_detail.ExtraPhoneDetailAPIView.as_view()),
    # banners
    path('<uuid:pk>/banner/new/', banner_create.BannerCreateAPIView.as_view()),
    path('<uuid:pk>/banner/list/', banner_list.BannerListAPIView.as_view()),
    path('<uuid:pk>/banner/detail/<int:banner_pk>/', banner_detail.BannerDetailAPIView.as_view()),
    # min cart cost
    path('<uuid:pk>/cart/rule/', min_cart_cost_update_create.MinCartCostCreateAPIView.as_view()),
    path('<uuid:pk>/cart/rule/<int:rule_pk>/', min_cart_cost_delete.MinCartCostDeleteAPIView.as_view()),

]
