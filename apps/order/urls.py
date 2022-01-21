from django.urls import path
from apps.order.api.cart_detail import CartAPIView
from apps.order.api.add_to_cart import AddToCartAPIView

app_name = 'order'

urlpatterns = [
    # customer добавленно в пути из-за проблем аунтентификации
    path('customer/cart/', CartAPIView.as_view()),  # нужно ли cart определять по своему id ?
    path('customer/add-to-cart/<str:product_slug>/', AddToCartAPIView.as_view()),
]
