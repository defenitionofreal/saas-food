from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.product.models import ModifierPrice, Product
from apps.product.serializers import ModifierPriceSerializer

from apps.company.models import Institution
from apps.company.services.compare_institution import _find_wrong_inst_id


class ModifierPriceDetailAPIView(APIView):
    """
    Retrieve, update or delete a modifier price.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, modifier_pk, modifier_price_pk):
        query = get_object_or_404(ModifierPrice.objects,
                                  user=self.request.user,
                                  modifier_id=modifier_pk,
                                  pk=modifier_price_pk)
        serializer = ModifierPriceSerializer(query)
        return Response(serializer.data)

    def put(self, request, modifier_pk, modifier_price_pk):
        query = get_object_or_404(ModifierPrice.objects,
                                  user=self.request.user,
                                  modifier_id=modifier_pk,
                                  pk=modifier_price_pk)
        product = Product.objects.filter(user=self.request.user)
        institution = Institution.objects.filter(user=self.request.user)

        if request.data["institution"]:
            if _find_wrong_inst_id(request.data["institution"],
                                   institution.values_list('id', flat=True)):
                return Response({"detail": f"wrong institution id"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "institution is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not request.data["product"] or request.data["product"] is None:
            return Response({"detail": "product is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data["product"] not in product.values_list('id',
                                                              flat=True):
            return Response({"detail": "wrong product id"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ModifierPriceSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, modifier_pk, modifier_price_pk):
        query = get_object_or_404(ModifierPrice.objects,
                                  user=self.request.user,
                                  modifier_id=modifier_pk,
                                  pk=modifier_price_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
