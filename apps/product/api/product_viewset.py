from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import ProductSerializer
from apps.product.models import Product
from apps.authentication.permissions import ConfirmedAccountPermission


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")
