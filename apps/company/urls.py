from django.urls import path
from .api import (institution_create,
                  institution_list,
                  institution_detail)

app_name = 'company'

urlpatterns = [
    path('institution/new/', institution_create.InstitutionCreateAPIView.as_view()),
    path('institution/list/', institution_list.InstitutionListAPIView.as_view()),
    path('institution/<uuid:pk>', institution_detail.InstitutionDetailAPIView.as_view()),
]
