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
                  working_hours_detail)

app_name = 'company'

urlpatterns = [
    # institution
    path('new/', institution_create.InstitutionCreateAPIView.as_view()),
    path('list/', institution_list.InstitutionListAPIView.as_view()),
    path('<uuid:pk>/', institution_detail.InstitutionDetailAPIView.as_view()),
    # design
    path('<uuid:pk>/design/new/', design_create.DesignCreateAPIView.as_view()),
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

]
