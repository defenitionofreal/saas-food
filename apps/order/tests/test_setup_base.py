from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.company.models.institution import Institution
from apps.delivery.models import Delivery, DeliveryInfo
from apps.delivery.models.enums import DeliveryType, SaleType
from apps.order.models import Bonus
from apps.product.models.category import Category

User = get_user_model()


class TestSetupBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_user()
        cls.create_institution()
        cls.create_category()

    @classmethod
    def create_user(cls):
        cls.user = User.objects.create(phone='+79111112233', email='t@mail.com', password='1')

    @classmethod
    def create_institution(cls):
        cls.institution = Institution.objects.create(user=cls.user, title='inst_1', description='d',
                                                     phone='+79111112233', domain='d.com')

    @classmethod
    def create_category(cls):
        cls.category = Category.objects.create(title='cat', slug='cat')

    def create_delivery_obj(self, sale_amount, sale_type: SaleType) -> Delivery:
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=sale_type, sale_amount=sale_amount)
        d.institution.set([self.institution])
        return d

    def create_delivery_info_obj(self, delivery: Delivery) -> DeliveryInfo:
        return DeliveryInfo.objects.create(type=delivery)

    def create_bonus(self, is_promo_code, write_off=100, accrual=100, is_active=True):
        return Bonus.objects.create(institution=self.institution, is_active=is_active, write_off=write_off,
                                    accrual=accrual, is_promo_code=is_promo_code)
