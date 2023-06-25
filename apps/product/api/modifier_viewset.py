from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.product.serializers import ModifierSerializer, ModifierPriceSerializer
from apps.product.models import Modifier, Product
from apps.authentication.permissions import ConfirmedAccountPermission


class ModifierViewSet(viewsets.ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = [IsAuthenticated, ConfirmedAccountPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # @action(methods=["get", "post", "put", "delete"])
    # def price(self, request, modifier_pk=None):
    #     """
    #
    #     """
    #     serializer = ModifierPriceSerializer(data=request.data)
    #     modifier = Modifier.objects.get(pk=modifier_pk)
    #     product_qs = Product.objects.filter(user=self.request.user)
    #     product = request.data.get("product", None)
    #
    #     if request.method == "POST":
    #
    #         if serializer.is_valid():
    #             serializer.save(user=self.request.user, modifier=modifier)
