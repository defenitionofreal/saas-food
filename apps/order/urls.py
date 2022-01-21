from django.urls import path
from apps.order.api.cart import CartAPIView
from apps.order.api.add_to_cart import AddToCartAPIView

app_name = 'order'
# cart достпуна по своему id
urlpatterns = [
    path('test/', CartAPIView.as_view()),
    # добавления в корзину
    path('customer/add-to-cart/<str:product_slug>', AddToCartAPIView.as_view()),
]