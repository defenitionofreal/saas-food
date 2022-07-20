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
