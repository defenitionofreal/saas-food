from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.models import Institution
from apps.delivery.serializers import DeliverySerializer
from apps.delivery.models import Delivery


class DeliveryDetailAPIView(APIView):
    """
    Retrieve, update or delete a delivery.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, delivery_pk):
        query = get_object_or_404(Delivery.objects,
                                  user=self.request.user,
                                  pk=delivery_pk)
        serializer = DeliverySerializer(query)
        return Response(serializer.data)

    def put(self, request, delivery_pk):
        institution = Institution.objects.filter(user=self.request.user)
        data = request.data["institution"]
        query = get_object_or_404(Delivery.objects,
                                  user=self.request.user,
                                  pk=delivery_pk)

        # if data:
        #     if _find_wrong_inst_id(data, institution.values_list('id',
        #                                                          flat=True)):
        #         return Response({"detail": f"wrong institution id"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        #     # TODO: разрешить менять тип но проверять если тип у других филиалов
        # else:
        #     return Response({"detail": "institution is required"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        serializer = DeliverySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, delivery_pk):
        query = get_object_or_404(Delivery.objects,
                                  user=self.request.user,
                                  pk=delivery_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
