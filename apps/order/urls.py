from django.urls import path
from apps.order.api.cart import CartAPIView
from apps.order.api.add_to_cart import AddToCartAPIView

app_name = 'order'
# cart достпуна по своему id
urlpatterns = [
    path('test/', CartAPIView.as_view()),
    # добавления в корзину /domain/add-to-cart/product-pk/
    path('add-to-cart/<int:product_id>', AddToCartAPIView.as_view()),
]