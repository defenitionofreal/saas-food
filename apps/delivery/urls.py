from django.urls import path
from .api import (delivery_create,
                  delivery_list,
                  delivery_detail)


app_name = 'delivery'

urlpatterns = [
   path('institution/<uuid:pk>/delivery/new/', delivery_create.DeliveryCreateAPIView.as_view()),
   path('institution/<uuid:pk>/delivery/list/', delivery_list.DeliveryListAPIView.as_view()),
   path('institution/<uuid:pk>/delivery/detail/<int:delivery_pk>/',delivery_detail.DeliveryDetailAPIView.as_view()),
]
