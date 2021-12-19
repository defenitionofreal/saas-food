from django.urls import path
from .api import (institution_create,
                  institution_list,
                  institution_detail,
                  design_create,
                  design_detail)

app_name = 'company'

urlpatterns = [
    # institution
    path('new/', institution_create.InstitutionCreateAPIView.as_view()),
    path('list/', institution_list.InstitutionListAPIView.as_view()),
    path('<uuid:pk>/', institution_detail.InstitutionDetailAPIView.as_view()),
    # design
    path('<uuid:pk>/design/new/', design_create.DesignCreateAPIView.as_view()),
    path('<uuid:pk>/design/detail/<int:design_pk>/', design_detail.DesignDetailAPIView.as_view()),
]
