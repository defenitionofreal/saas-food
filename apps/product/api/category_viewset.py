from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import CategorySerializer
from apps.product.models import Category
from apps.authentication.permissions import ConfirmedAccountPermission


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
