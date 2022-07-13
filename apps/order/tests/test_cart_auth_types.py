from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from apps.company.models.institution import Institution
from apps.order.models import Cart, CartItem
import apps.order.models.cart_keys as cart_keys
from apps.order.services.generate_cart_key import _generate_cart_key
from apps.order.services.product_obj_to_cart_item_dict import \
    get_cart_item_dict_from_product_object_no_modifiers_no_additives
from apps.product.models import Product
from apps.product.models.category import Category
from rest_framework.response import Response
from django.conf import settings

User = get_user_model()

domain = 'test'
api_path = f'/api/showcase/{domain}/order/customer/cart/'
test_api = 'api/showcase/test/'
test_user = 'api/auth/user/'
test_login_phone = 'api/auth/login/phone/'


def add_product_to_cart_no_mod_and_additives(cart: Cart, product: Product, quantity=1):
    d = get_cart_item_dict_from_product_object_no_modifiers_no_additives(product)
    cart.add_product_to_cart_as_product_dict(d, quantity)


class TestCartRetrieveExistingUser(APITestCase):
    product1_price = 50
    product2_price = 100
    quantity_p1 = 1
    quantity_p2 = 2
    domain = domain
    user_phone = '+79111112233'
    user_password = '1'

    @classmethod
    def setUpTestData(cls):
        cls.create_user_and_client()
        cls.create_institution()
        cls.create_category()
        cls.create_products()

    @classmethod
    def create_user_and_client(cls):
        cls.user: User = User.objects.create(phone=cls.user_phone, email='t@mail.com', password=cls.user_password)
        cls.client: APIClient = APIClient()

    @classmethod
    def create_institution(cls):
        cls.institution = Institution.objects.create(user=cls.user, title='inst_1', description='d',
                                                     phone='+79111112233', domain=cls.domain)

    @classmethod
    def create_category(cls):
        cls.category = Category.objects.create(title='cat', slug='cat')

    @classmethod
    def create_products(cls):
        cls.prod1 = Product.objects.create(category=cls.category, title='prod1', description='d',
                                           price=cls.product1_price,
                                           weight=1, cook_time=1, slug='p1')
        cls.prod2 = Product.objects.create(category=cls.category, title='prod2', description='d',
                                           price=cls.product2_price,
                                           weight=1, cook_time=1, slug='p2')

    def force_auth_user(self):
        self.client.force_authenticate(self.user)

    def logout_user(self):
        self.client.logout()

    def create_empty_cart(self):
        cart = Cart.objects.create(institution=self.institution)
        cart.save()
        return cart

    def test_no_auth_no_cart_in_db_has_cart_in_session_login(self):
        """
        When no cart in DB for user and he creates guest cart then login:
        1. Assign guest cart to this user
        2. Cart content is invisible by this session id after logout
        """
        s_id = refresh_cart_session_id(self)

        cart = Cart.objects.create(institution=self.institution)
        add_product_to_cart_no_mod_and_additives(cart, self.prod1, 5)

        cart_id = cart.id
        cart.session_id = s_id
        cart.save()

        # NO AUTH

        resp1: Response = self.client.get(api_path)
        response_1 = resp1.data
        self.assertEqual(response_1[cart_keys.customer], None)
        self.assertEqual(response_1[cart_keys.id], cart_id)

        # LOGIN

        self.force_auth_user()
        user_id = self.user.id
        resp2: Response = self.client.get(api_path)
        response_2 = resp2.data
        self.assertEqual(response_2[cart_keys.id], cart_id)
        self.assertEqual(response_2[cart_keys.customer], user_id)

        # LOGOUT

        self.logout_user()

        resp3: Response = self.client.get(api_path)
        response_3 = resp3.data
        self.assertTrue(cart_keys.id not in response_3)
        self.assertTrue(cart_keys.customer not in response_3)

    def test_login_without_session_cart_and_has_db_cart(self):
        """
          1. Returns cart from database assigned to this customer
          2. Not shows this cart with this session id when logout
        """
        s_id = refresh_cart_session_id(self)

        cart: Cart = Cart.objects.create(institution=self.institution)
        add_product_to_cart_no_mod_and_additives(cart, self.prod1, 5)

        cart_id = cart.id
        cart.session_id = s_id
        cart.customer = self.user
        cart.save()

        # NO AUTH

        resp1: Response = self.client.get(api_path)
        response_1 = resp1.data
        self.assertTrue(cart_keys.id not in response_1)
        self.assertTrue(cart_keys.customer not in response_1)

        # AUTH

        self.force_auth_user()
        user_id = self.user.id
        resp2: Response = self.client.get(api_path)
        response_2 = resp2.data
        self.assertEqual(response_2[cart_keys.id], cart_id)
        self.assertEqual(response_2[cart_keys.customer], user_id)

        self.logout_user()

    def test_no_auth_has_cart_in_db_has_cart_in_session_login(self):
        """
        Merges two carts (db and session) on login
        1. DB cart is modified and returned
        2. Session cart is removed
        """
        s_id = refresh_cart_session_id(self)

        # setup db cart
        db_cart: Cart = Cart.objects.create(institution=self.institution)
        add_product_to_cart_no_mod_and_additives(db_cart, self.prod1, 5)

        db_cart_id = db_cart.id
        db_cart.customer = self.user
        db_cart.save()

        # setup session cart
        session_cart: Cart = Cart.objects.create(institution=self.institution)
        session_cart.session_id = s_id
        add_product_to_cart_no_mod_and_additives(db_cart, self.prod1, 2)
        add_product_to_cart_no_mod_and_additives(db_cart, self.prod2, 1)

        session_cart_id = session_cart.id

        # NO AUTH

        resp1: Response = self.client.get(api_path)
        response_1 = resp1.data
        self.assertEqual(response_1[cart_keys.id], session_cart_id)
        self.assertEqual(response_1[cart_keys.customer], None)

        # AUTH

        self.force_auth_user()
        resp2: Response = self.client.get(api_path)
        response_2 = resp2.data
        print(response_2)


def refresh_cart_session_id(testclass: TestCartRetrieveExistingUser):
    """this functionality doesn't work when placed inside class"""
    session = testclass.client.session
    s_id = _generate_cart_key()
    session[settings.CART_SESSION_ID] = s_id
    session.save()
    return s_id
