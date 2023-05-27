from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.delivery.models import DeliveryZone, DeliveryZoneСoordinates
from apps.company.models import Institution


class DeliveryZoneCreateAPIView(APIView):
    """ Create new delivery zone """
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = self.request.user
        institution = Institution.objects.filter(user=user)
        # get array values
        request_institution = request.data["institution"]
        title = request.data["title"]
        price = request.data["price"]
        min_order_amount = request.data["min_order_amount"]
        free_delivery_amount = request.data["free_delivery_amount"]
        delivery_time = request.data["delivery_time"]
        coordinates = request.data["coordinates"]

        # if request_institution:
        #     if _find_wrong_inst_id(request_institution,
        #                            institution.values_list('id', flat=True)):
        #         return Response({"detail": f"wrong institution id"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"detail": "institution is required"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        if not title:
            return Response({"detail": "title is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not coordinates:
            return Response({"detail": "coordinates are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        delivery_zone, zone_created = DeliveryZone.objects.get_or_create(
            institution=institution.filter(id=request_institution[0]).first(),
            title=title,
            price=price,
            min_order_amount=min_order_amount,
            free_delivery_amount=free_delivery_amount,
            delivery_time=delivery_time)

        if zone_created is True:
            DeliveryZoneСoordinates.objects.create(zone=delivery_zone,
                                                   coordinates=coordinates)

        return Response({"detail": "delivery zone created"},
                        status=status.HTTP_201_CREATED)
