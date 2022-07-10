from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.company.models.institution import Institution
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
