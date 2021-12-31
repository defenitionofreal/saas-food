from django.urls import path
from .api import (delivery_create,
                  delivery_list,
                  delivery_detail,
                  delivery_zone_file_create)


app_name = 'delivery'

urlpatterns = [
    # delivery
   path('institution/<uuid:pk>/delivery/new/', delivery_create.DeliveryCreateAPIView.as_view()),
   path('institution/<uuid:pk>/delivery/list/', delivery_list.DeliveryListAPIView.as_view()),
   path('institution/<uuid:pk>/delivery/detail/<int:delivery_pk>/',delivery_detail.DeliveryDetailAPIView.as_view()),
    # delivery zone file
   path('institution/<uuid:pk>/delivery-zone/file/new/', delivery_zone_file_create.DeliveryZoneFileCreateAPIView.as_view()),
]
