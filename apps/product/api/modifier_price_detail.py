from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.product.models import ModifierPrice
from apps.product.serializers import ModifierPriceSerializer


class ModifierPriceDetailAPIView(APIView):
    """
    Retrieve, update or delete a modifier price.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, modifier_pk, modifier_price_pk):
        query = get_object_or_404(ModifierPrice.objects, institution_id=pk, modifier_id=modifier_pk, pk=modifier_price_pk)
        serializer = ModifierPriceSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, modifier_pk, modifier_price_pk):
        query = get_object_or_404(ModifierPrice.objects, institution_id=pk, modifier_id=modifier_pk, pk=modifier_price_pk)
        serializer = ModifierPriceSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, modifier_pk, modifier_price_pk):
        query = get_object_or_404(ModifierPrice.objects, institution_id=pk, modifier_id=modifier_pk, pk=modifier_price_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
