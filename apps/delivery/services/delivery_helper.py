from apps.delivery.models.enums import SaleType, DeliveryType
from apps.order.services.math_utils import get_absolute_from_percent_and_total

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
import json


class DeliveryHelper:
    def __init__(self, delivery_info):
        self.delivery = delivery_info

    @property
    def is_valid(self):
        return self.delivery is not None

    def _get_institution(self):
        if self.is_valid:
            return self.delivery.type.institution.first()

    def get_sale_type(self):
        if self.is_valid:
            return self.delivery.type.sale_type

    @property
    def is_absolute_sale_type(self):
        return self.get_sale_type() == SaleType.ABSOLUTE

    @property
    def is_percent_sale_type(self):
        return self.get_sale_type() == SaleType.PERCENT

    @property
    def delivery_price(self) -> [int, None]:
        if self.is_valid:
            return self.delivery.type.delivery_price

    @property
    def free_delivery_amount(self) -> [int, None]:
        if self.is_valid:
            return self.delivery.type.free_delivery_amount

    @property
    def min_delivery_order_amount(self) -> [int, None]:
        if self.is_valid:
            return self.delivery.type.min_order_amount

    @property
    def sale_amount(self):
        if self.is_valid:
            return self.delivery.type.sale_amount

    def get_delivery_sale(self, cart_total) -> [int, None]:
        if self.is_valid:
            delivery_sale = self.sale_amount
            if delivery_sale:
                if self.is_absolute_sale_type:
                    return delivery_sale
                if self.is_percent_sale_type:
                    return get_absolute_from_percent_and_total(delivery_sale, cart_total)

    @property
    def get_delivery_zone(self):
        institution = self._get_institution()
        zones = institution.dz.filter(is_active=True)
        if zones.exists() and self.delivery.type.delivery_type == DeliveryType.COURIER:
            for zone in zones:
                address = self.delivery.address.address
                point = Point([json.loads(address.latitude),
                               json.loads(address.longitude)])
                polygon = Polygon(json.loads(
                    zone.dz_coordinates.values_list("coordinates",
                                                    flat=True)[0]))
                if boolean_point_in_polygon(point, polygon):
                    return {"title": zone.title,
                            "price": zone.price,
                            "free_delivery_amount": zone.free_delivery_amount,
                            "min_order_amount": zone.min_order_amount,
                            "delivery_time": zone.delivery_time}
        return None

    def calculate_price_for_delivery_zone(self, cart_current_price: int):
        if not self.get_delivery_zone:
            return 0
        if self.get_delivery_zone["free_delivery_amount"]:
            if cart_current_price < self.get_delivery_zone["free_delivery_amount"]:
                return self.get_delivery_zone["price"]
        else:
            return self.get_delivery_zone["price"]

    def calculate_final_delivery_price(self, cart_current_price: int):
        total = 0

        delivery_price = self.delivery_price
        free_delivery_amount = self.free_delivery_amount

        if self.get_delivery_zone:
            total = self.calculate_price_for_delivery_zone(cart_current_price)
        else:
            if free_delivery_amount:
                if cart_current_price < free_delivery_amount:
                    total += cart_current_price
            else:
                if delivery_price:
                    total += delivery_price

        delivery_sale = self.get_delivery_sale(cart_current_price)
        if delivery_sale:
            total -= delivery_sale

        return total
