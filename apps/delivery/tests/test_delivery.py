from apps.delivery.models import Delivery
from apps.delivery.models.enums import DeliveryType
from apps.delivery.services.delivery_helper import DeliveryHelper
from apps.delivery.tests.test_delivery_setup import TestDeliverySetup


class TestDeliveryHelper(TestDeliverySetup):

    def test_delivery_can_get_institution(self):
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=50,
                                    sale_amount=100)
        d.institution.set([self.institution])
        d.save()
        delivery_info = self.create_delivery_info_obj(d)

        delivery = DeliveryHelper(delivery_info=delivery_info)
        self.assertEqual(delivery._get_institution(), self.institution)

    def test_calculate_price_for_delivery_zone(self):
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=50,
                                    sale_amount=100)
        d.institution.set([self.institution])
        d.save()
        delivery_info = self.create_delivery_info_obj(d)

        zone_delivery_price = 100
        min_order_amount = 150
        free_delivery_amount = 300
        delivery_zone = self.create_delivery_zone_obj(price=zone_delivery_price,
                                                      min_order_amount=min_order_amount,
                                                      free_delivery_amount=free_delivery_amount)
        delivery_zone.save()
        delivery = DeliveryHelper(delivery_info=delivery_info)

        # test cart_price less free_delivery_amount

        cart_price_less_fda = int(free_delivery_amount * 0.5)
        dz_price_fda_less = delivery.calculate_price_for_delivery_zone(cart_price_less_fda)
        self.assertEqual(dz_price_fda_less, zone_delivery_price)

        # test cart_price equal free_delivery_amount

        cart_price_equal_fda = free_delivery_amount
        dz_price_fda_equal = delivery.calculate_price_for_delivery_zone(cart_price_equal_fda)
        self.assertEqual(dz_price_fda_equal, 0)

        # test cart_price greater free_delivery_amount

        cart_price_greater_fda = free_delivery_amount * 2
        dz_price_fda_greater = delivery.calculate_price_for_delivery_zone(cart_price_greater_fda)
        self.assertEqual(dz_price_fda_greater, 0)


        # todo: uncomment later
        # # test no free delivery amount
        #
        # delivery_zone.free_delivery_amount = None
        # delivery_zone.save()
        #
        # dz_no_free_amount  = delivery.calculate_price_for_delivery_zone(10000000)
        # self.assertEqual(dz_no_free_amount, zone_delivery_price)


