from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.company.models import Institution
from apps.order.models import Cart
from apps.delivery.models import DeliveryInfo
from apps.delivery.models.enums import DeliveryType
from apps.location.models import Address, AddressLink
from apps.order.services.generate_cart_key import _generate_cart_key

from django.conf import settings

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

import json

#
# class DeliveryInfoAPIView(APIView):
#     """
#     Delivery info create by customer
#     """
#
#     def post(self, request, domain):
#         institution = Institution.objects.get(domain=domain)
#         address = request.data['address']
#         order_date = request.data['order_date']
#         delivery_type = request.data['delivery_type']
#
#         if delivery_type in institution.delivery.values_list("delivery_type",
#                                                              flat=True):
#             delivery_type = institution.delivery.get(
#                 delivery_type=request.data['delivery_type'])
#         else:
#             return Response({"detail": "Wrong delivery type"},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         session = self.request.session
#         if not settings.DELIVERY_SESSION_ID in session:
#             session[settings.DELIVERY_SESSION_ID] = _generate_cart_key()
#         else:
#             session[settings.DELIVERY_SESSION_ID]
#         session.modified = True
#         delivery_session = session[settings.DELIVERY_SESSION_ID]
#
#         if delivery_session:
#             address_arr = {"city": address["city"],
#                            "region": address["region"],
#                            "street": address["street"],
#                            "building": address["building"],
#                            "office": address["office"],
#                            "floor": address["floor"],
#                            "latitude": address["latitude"],
#                            "longitude": address["longitude"]}
#             delivery_session = {"delivery_type": delivery_type.delivery_type,
#                                 "order_date": order_date,
#                                 "address": address_arr}
#
#             # cart check
#             if settings.CART_SESSION_ID in session:
#                 session_cart = Cart.objects.filter(
#                     institution=institution,
#                     session_id=session[settings.CART_SESSION_ID]).first()
#                 if session_cart:
#                     session_cart.delivery = delivery_session
#                     session_cart.save()
#
#             return Response(
#                 {"detail": delivery_session},
#                 status=status.HTTP_201_CREATED
#             )


class DeliveryInfoAPIView(APIView):
    """
    Delivery info create by customer
    """

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        address = request.data['address']
        order_date = request.data['order_date']
        delivery_type = request.data['delivery_type']

        if delivery_type in institution.delivery.values_list("delivery_type",
                                                             flat=True):
            delivery_type = institution.delivery.get(
                delivery_type=delivery_type)

            # check if customers point in delivery area
            if delivery_type.delivery_type == DeliveryType.COURIER:
                zones = institution.dz.filter(is_active=True)
                if zones.exists() and not any(boolean_point_in_polygon(
                            Point([json.loads(address["latitude"]),
                                   json.loads(address["longitude"])]),
                            Polygon(json.loads(zone.dz_coordinates.values_list(
                                "coordinates", flat=True)[0])))
                               for zone in zones):
                    return Response({"detail": "Point not in delivery zone"})
        else:
            return Response({"detail": "Wrong delivery type"},
                            status=status.HTTP_400_BAD_REQUEST)

        session = self.request.session
        if settings.DELIVERY_SESSION_ID not in session:
            session[settings.DELIVERY_SESSION_ID] = _generate_cart_key()
        else:
            session[settings.DELIVERY_SESSION_ID]
        session.modified = True
        delivery_session = session

        if delivery_session:
            address_obj = Address.objects.create(
                city=address["city"],
                region=address["region"],
                street=address["street"],
                building=address["building"],
                office=address["office"],
                floor=address["floor"],
                latitude=address["latitude"],
                longitude=address["longitude"]
            )
            if user.is_authenticated:
                address_link, address_link_created = AddressLink.objects \
                    .update_or_create(user=user,
                                      defaults={"address": address_obj})

                delivery_info, delivery_info_created = DeliveryInfo.objects\
                    .update_or_create(user=user,
                                      defaults={"type": delivery_type,
                                                "address": address_link,
                                                "order_date": order_date})
                # cart check here
                cart = Cart.objects.filter(institution=institution,
                                           customer=user).first()
                if cart:
                    cart.delivery = delivery_info
                    cart.save()
            else:
                address_link, address_link_created = AddressLink.objects \
                    .update_or_create(
                        session_id=session[settings.DELIVERY_SESSION_ID],
                        defaults={"address": address_obj})

                delivery_info, delivery_info_created = DeliveryInfo.objects \
                    .update_or_create(
                        session_id=session[settings.DELIVERY_SESSION_ID],
                        defaults={"type": delivery_type,
                                  "address": address_link,
                                  "order_date": order_date})
                # cart check
                if settings.CART_SESSION_ID in session:
                    session_cart = Cart.objects.filter(
                        institution=institution,
                        session_id=session[settings.CART_SESSION_ID]).first()
                    if session_cart:
                        session_cart.delivery = delivery_info
                        session_cart.save()

            if delivery_info_created:
                return Response({"detail": "Delivery information created"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Delivery information updated"},
                                status=status.HTTP_201_CREATED)
