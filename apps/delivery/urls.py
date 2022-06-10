from django.urls import path
from .api.organization import (delivery_create,
                               delivery_detail,
                               delivery_list,
                               delivery_zone_file_create,
                               delivery_zone_create)

app_name = 'delivery'

urlpatterns = [
    # organization views
    path('delivery/new/', delivery_create.DeliveryCreateAPIView.as_view()),
    path('delivery/list/', delivery_list.DeliveryListAPIView.as_view()),
    path('delivery/detail/<int:delivery_pk>/', delivery_detail.DeliveryDetailAPIView.as_view()),
    # delivery zones
    path('delivery-zone/new/', delivery_zone_create.DeliveryZoneCreateAPIView.as_view()),
    # delivery zones file (stopped for a while!)
    path('institution/<uuid:pk>/delivery-zone/file/new/', delivery_zone_file_create.DeliveryZoneFileCreateAPIView.as_view()),
]
