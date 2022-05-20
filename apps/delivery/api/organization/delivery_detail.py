from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.delivery.serializers import DeliverySerializer
from apps.delivery.models import Delivery


class DeliveryDetailAPIView(APIView):
    """
    Retrieve, update or delete a delivery.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, delivery_pk):
        query = get_object_or_404(Delivery.objects, institution_id=pk, pk=delivery_pk)
        serializer = DeliverySerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, delivery_pk):
        query = get_object_or_404(Delivery.objects, institution_id=pk, pk=delivery_pk)
        serializer = DeliverySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, delivery_pk):
        query = get_object_or_404(Delivery.objects, institution_id=pk, pk=delivery_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
