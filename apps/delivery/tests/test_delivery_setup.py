from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.company.models import Institution
from apps.delivery.models import Delivery, DeliveryInfo
from apps.delivery.models.enums import SaleType, DeliveryType

User = get_user_model()

domain = 'test'


class TestDeliverySetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_user()
        cls.create_institution()

    @classmethod
    def create_user(cls):
        cls.user = User.objects.create(phone='+79111112233', email='t@mail.com', password='1')

    @classmethod
    def create_institution(cls):
        cls.institution = Institution.objects.create(user=cls.user, title='inst_1', description='d',
                                                     phone='+79111112233', domain=domain)

    def create_delivery_obj(self, sale_amount, sale_type: SaleType) -> Delivery:
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=sale_type,
                                    sale_amount=sale_amount)
        d.institution.set([self.institution])
        return d

    def create_delivery_info_obj(self, delivery: Delivery) -> DeliveryInfo:
        return DeliveryInfo.objects.create(type=delivery)
