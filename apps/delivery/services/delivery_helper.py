from apps.delivery.models.enums import SaleType
from apps.order.services.math_utils import get_absolute_from_percent_and_total


class DeliveryHelper:
    def __init__(self, delivery_info):
        self.delivery = delivery_info

    @property
    def is_valid(self):
        return self.delivery is not None

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
