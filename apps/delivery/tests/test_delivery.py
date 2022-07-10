from apps.delivery.models.enums import DeliveryType, SaleType
from apps.delivery.tests.test_setup_base import TestSetupBase
from apps.delivery.models import Delivery


class TestDelivery(TestSetupBase):

    def create_delivery_obj(self, sale_amount, sale_type: SaleType) -> Delivery:
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=sale_type, sale_amount=sale_amount)
        d.institution.set([self.get_institution()])
        return d

    def test_absolute_delivery_discount(self):
        sale_amount = 50
        order_price = 70
        abs_delivery = self.create_delivery_obj(sale_amount, SaleType.ABSOLUTE)
        discount = abs_delivery.get_delivery_discount(order_price)
        self.assertEqual(discount, sale_amount)

    def test_percent_delivery_discount(self):
        sale_amount = 50
        order_price = 20
        percent_delivery = self.create_delivery_obj(sale_amount, SaleType.PERCENT)
        discount = percent_delivery.get_delivery_discount(order_price)
        self.assertEqual(discount, 10)
