from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.delivery.models import Delivery
from apps.delivery.serializers import DeliverySerializer
from apps.company.models import Institution


class DeliveryCreateAPIView(APIView):
    """ Create new delivery """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)
        institution = Institution.objects.filter(user=self.request.user)
        delivery = Delivery.objects.filter(user=self.request.user)
        affiliate_data = request.data["institution"]

        # если нету филиала в запросе
        if not affiliate_data:
            return Response({"detail": "institution is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # # если есть невреный uuid филила
        # if _find_wrong_inst_id(affiliate_data,
        #                        institution.values_list('id', flat=True)):
        #     return Response({"detail": f"wrong institution id"},
        #                     status=status.HTTP_400_BAD_REQUEST)
        #
        # # если есть дубликаты типов доставки в филиале
        # if _check_duplicated_uuid(
        #         affiliate_data, delivery.values_list('institution', flat=True)):
        #     if request.data["delivery_type"] in delivery.values_list('delivery_type', flat=True):
        #         return Response({"detail": f"institution has delivery type"},
        #                         status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            instance = serializer.save(user=self.request.user)
            instance.institution.add(*affiliate_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
