from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.company.models import Institution
from apps.delivery.models import Delivery, DeliveryInfo, DeliveryZone, DeliveryZoneСoordinates
from apps.delivery.models.enums import SaleType, DeliveryType
from apps.location.models import Address, AddressLink

User = get_user_model()

domain = 'test'


class TestDeliverySetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_user()
        cls.create_institution()
        cls.create_address()

    @classmethod
    def create_user(cls):
        cls.user = User.objects.create(phone='+79111112233', email='t@mail.com', password='1')

    @classmethod
    def create_institution(cls):
        cls.institution = Institution.objects.create(user=cls.user, title='inst_1', description='d',
                                                     phone='+79111112233', domain=domain)

    @classmethod
    def create_address(cls):
        cls.address = Address.objects.create(city='default', region='r', street='street',
                                             building='1', latitude='37.629968', longitude='55.761219')
        cls.address_link = AddressLink.objects.create(user=cls.user, institution=cls.institution, address=cls.address)

    def create_delivery_obj(self, sale_amount, sale_type: SaleType) -> Delivery:
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=sale_type,
                                    sale_amount=sale_amount)
        d.institution.set([self.institution])
        return d

    def create_delivery_info_obj(self, delivery: Delivery) -> DeliveryInfo:
        return DeliveryInfo.objects.create(type=delivery, address=self.address_link)

    def create_delivery_zone_obj(self, price, min_order_amount, free_delivery_amount, title='delivery_zone'):
        dz = DeliveryZone.objects.create(institution=self.institution,
                                         price=price,
                                         min_order_amount=min_order_amount,
                                         free_delivery_amount=free_delivery_amount,
                                         title=title)
        coordinates = '[[ [ 37.61507468202977, 55.76797072219127 ], ' \
                      '[ 37.60993804221867, 55.74562109508482 ], ' \
                      '[ 37.649151288418906, 55.74495799748623 ], ' \
                      '[ 37.647581672276246, 55.7717111831524 ] ]]'
        DeliveryZoneСoordinates.objects.create(zone=dz, coordinates=coordinates)
        return dz
