from django.urls import path
from .api import (institution_create,
                  institution_list,
                  institution_detail)

app_name = 'company'

urlpatterns = [
    path('new/', institution_create.InstitutionCreateAPIView.as_view()),
    path('list/', institution_list.InstitutionListAPIView.as_view()),
    path('<uuid:pk>', institution_detail.InstitutionDetailAPIView.as_view()),
]
