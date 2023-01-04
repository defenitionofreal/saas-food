# apps
from apps.location.models import Address, AddressLink
from apps.delivery.models.enums import DeliveryType
from apps.delivery.models import DeliveryInfo
# rest framework
from rest_framework.response import Response
from rest_framework import status
# other
from django.utils import timezone
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
import json


class DeliveryHelper:

    def __init__(self,
                 request,
                 affiliate: object,
                 delivery_type: str,
                 address: dict,
                 user,
                 session,
                 order_date):
        self.request = request
        self.affiliate = affiliate
        self.delivery_type = delivery_type
        # адрес из формы (в форму автоматом ставится адрес юзера)
        self.address = address
        self.user = user
        self.session = session

        self.order_date = order_date

    def _get_order_date(self):
        date = self.order_date
        if date is None or date == "":
            date = timezone.now()
        return date

    def _check_delivery_type(self):
        """ если тип доставки входит в выбранные типы филиала """
        if self.delivery_type in self.affiliate.delivery.values_list("delivery_type", flat=True):
            return self.delivery_type
        return None

    def _get_address_link(self):
        """ возвращаю ссылку на адресс юзера/гостя """
        address_obj, _ = Address.objects.get_or_create(
            city=self.address["city"],
            region=self.address["region"],
            street=self.address["street"],
            building=self.address["building"],
            office=self.address["office"],
            floor=self.address["floor"],
            latitude=self.address["latitude"],
            longitude=self.address["longitude"]
        )
        if self.user.is_authenticated:
            address_link, _ = AddressLink.objects.get_or_create(
                user=self.user,
                address=address_obj
            )
        else:
            address_link, _ = AddressLink.objects.get_or_create(
                    session_id=self.session,
                    address=address_obj
            )
        return address_link

    def _get_delivery_info(self, delivery_type, address_link):
        """ возвращаю инфо доставки юзера (обновляю или создаю) """

        defaults = {"type": delivery_type,
                    "address": address_link,
                    "order_date": self._get_order_date()}

        if self.user.is_authenticated:
            session_delivery = DeliveryInfo.objects.filter(session_id=self.session)
            if session_delivery.exists():
                delivery_info = session_delivery.first()
                delivery_info.user = self.user
                delivery_info.type = delivery_type
                delivery_info.address = address_link
                delivery_info.order_date = self._get_order_date()
                delivery_info.save()
            else:
                delivery_info, _ = DeliveryInfo.objects.update_or_create(
                    user=self.user,
                    defaults=defaults
                )
        else:
            delivery_info, _ = DeliveryInfo.objects.update_or_create(
                session_id=self.session,
                defaults=defaults
            )
        return delivery_info

    def check_delivery_zones(self) -> bool:
        """ проверка на зоны доставки филилалы, если есть """
        zones = self.affiliate.dz.filter(is_active=True)
        if zones.exists() and not any(boolean_point_in_polygon(
                Point(
                    [json.loads(self.address["latitude"]),
                     json.loads(self.address["longitude"])]
                      ),
                Polygon(
                    json.loads(zone.dz_coordinates.values_list(
                        "coordinates", flat=True)[0])
                     )
                ) for zone in zones):
            return False
        return True

    def get_pick_up_type_address_link(self, delivery):
        """ возвращает адрес филиала при типе с собой/в зале """
        if delivery.delivery_type in [DeliveryType.PICKUP, DeliveryType.INDOOR]:
            address_link = self.affiliate.addresslink_set.first()
            return address_link
        return None

    def get_courier_type_address_link(self, delivery):
        """ возвращаю адресс юзера """
        if delivery.delivery_type == DeliveryType.COURIER:
            if self.check_delivery_zones() is True:
                address_link = self._get_address_link()
                return address_link
        return None

    def set_delivery_info(self):
        delivery_type = self._check_delivery_type()
        if delivery_type is None:
            return Response({"detail": "Wrong delivery type"},
                            status=status.HTTP_400_BAD_REQUEST)

        affiliate_delivery = self.affiliate.delivery.get(
            delivery_type=delivery_type
        )

        address = self.get_pick_up_type_address_link(affiliate_delivery)
        if address is None:
            address = self.get_courier_type_address_link(affiliate_delivery)
        if address is None:
            return Response({"detail": "Check delivery zones"},
                            status=status.HTTP_400_BAD_REQUEST)

        self._get_delivery_info(affiliate_delivery, address)

        return Response({"detail": "Delivery information created"},
                        status=status.HTTP_201_CREATED)
