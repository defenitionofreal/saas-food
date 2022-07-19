from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from apps.company.models import Institution
from apps.delivery.models import DeliveryInfo, Delivery
from apps.delivery.models.enums import SaleType, DeliveryType
from apps.order.models import Bonus
from apps.product.models import Category, Product

User = get_user_model()

domain = 'test'


class TestSetupBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_client()
        cls.create_user()
        cls.create_anonymous_user()
        cls.create_institution()
        cls.create_category()

    @classmethod
    def create_user(cls):
        cls.user = User.objects.create(phone='+79111112233', email='t@mail.com', password='1')

    @classmethod
    def create_anonymous_user(cls):
        cls.anon_user = auth.get_user(cls.client)

    @classmethod
    def create_client(cls):
        cls.client: APIClient = APIClient()

    def force_auth_user(self):
        self.client.force_authenticate(self.user)

    def logout_user(self):
        self.client.logout()

    @classmethod
    def create_institution(cls):
        cls.institution = Institution.objects.create(user=cls.user, title='inst_1', description='d',
                                                     phone='+79111112233', domain=domain)

    @classmethod
    def create_category(cls):
        cls.category = Category.objects.create(title='cat', slug='cat')

    def create_bonus(self, is_promo_code, write_off=100, accrual=100, is_active=True):
        return Bonus.objects.create(institution=self.institution, is_active=is_active, write_off=write_off,
                                    accrual=accrual, is_promo_code=is_promo_code)

    @classmethod
    def create_simple_product(cls, title, price, slug):
        # maybe get or create
        return Product.objects.create(category=cls.category, title=title, description='d', price=price,
                                      weight=1, cook_time=1, slug=slug)

    def create_delivery_obj(self, sale_amount, sale_type: SaleType) -> Delivery:
        d = Delivery.objects.create(delivery_type=DeliveryType.COURIER,
                                    sale_type=sale_type,
                                    sale_amount=sale_amount)
        d.institution.set([self.institution])
        return d

    def create_delivery_info_obj(self, delivery: Delivery) -> DeliveryInfo:
        return DeliveryInfo.objects.create(type=delivery)

