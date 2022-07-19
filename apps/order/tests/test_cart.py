from apps.delivery.models.enums import SaleType
from apps.order.models import Cart, CartItem
from apps.order.services.cart_helper import CartHelper
from apps.order.services.product_obj_to_cart_item_dict import get_cart_item_dict_from_product
from apps.order.tests.dummy_request import DummyRequest
from apps.order.tests.test_cart_setup import TestSetupBase


class TestCart(TestSetupBase):
    product1_price = 50
    product2_price = 100
    quantity_p1 = 1
    quantity_p2 = 2

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_products()
        cls.create_cart()

    @classmethod
    def create_products(cls):
        cls.prod1 = cls.create_simple_product(title='prod1', price=cls.product1_price, slug='p1')
        cls.prod2 = cls.create_simple_product(title='prod2', price=cls.product2_price, slug='p2')

    @classmethod
    def create_cart(cls):
        cls.cart = Cart.objects.create(institution=cls.institution)
        prod1_dict = get_cart_item_dict_from_product(cls.prod1)
        prod2_dict = get_cart_item_dict_from_product(cls.prod2)

        cls.cart_item1 = CartItem.objects.create(cart=cls.cart, product=prod1_dict, quantity=cls.quantity_p1)
        cls.cart_item2 = CartItem.objects.create(cart=cls.cart, product=prod2_dict, quantity=cls.quantity_p2)

        cls.cart.items.set([cls.cart_item1, cls.cart_item2])

    def get_cart(self) -> Cart:
        return self.cart

    def get_basic_total_cart_price(self):
        return self.product1_price * self.quantity_p1 + self.product2_price * self.quantity_p2

    def test_cart_delivery_data(self):
        request = DummyRequest(user=self.anon_user, generate_cart_id=True)
        db_cart = self.get_cart()
        db_cart.session_id = request.get_cart_session_id()

        delivery_sale = 25
        delivery_sale_type = SaleType.ABSOLUTE
        delivery = self.create_delivery_obj(delivery_sale, delivery_sale_type)
        delivery_info = self.create_delivery_info_obj(delivery)
        delivery.delivery_price = 123
        delivery.free_delivery_amount = 555
        delivery.min_order_amount = 9
        delivery.save()
        db_cart.delivery = delivery_info
        db_cart.save()

        cart = CartHelper(request, self.institution)

        self.assertEqual(cart.get_delivery_price, delivery.delivery_price)
        self.assertEqual(cart.get_free_delivery_amount, delivery.free_delivery_amount)
        self.assertEqual(cart.get_min_delivery_order_amount, delivery.min_order_amount)

    def test_customer_bonus_contribution_to_sale(self):
        request = DummyRequest(user=self.anon_user, generate_cart_id=True)
        db_cart = self.get_cart()
        db_cart.session_id = request.get_cart_session_id()

        customer_bonus = 30
        db_cart.bonus = self.create_bonus(is_promo_code=True)
        db_cart.customer_bonus = customer_bonus
        db_cart.save()

        cart = CartHelper(request, self.institution)

        self.assertEqual(cart.get_customer_bonus_contribution_to_sale(), customer_bonus)

    def test_get_total_cart_after_sale(self):
        request = DummyRequest(user=self.anon_user, generate_cart_id=True)
        db_cart = self.get_cart()
        db_cart.session_id = request.get_cart_session_id()

        customer_bonus = 30
        db_cart.bonus = self.create_bonus(is_promo_code=True)
        db_cart.customer_bonus = customer_bonus
        db_cart.save()

        cart = CartHelper(request, self.institution)

        total_cart = self.get_basic_total_cart_price()
        expected_after_sale = total_cart - customer_bonus

        self.assertEqual(cart.get_total_cart_after_sale, expected_after_sale)

    def test_get_total_cart(self):
        request = DummyRequest(user=self.anon_user, generate_cart_id=True)
        db_cart = self.get_cart()
        db_cart.session_id = request.get_cart_session_id()
        db_cart.save()
        cart = CartHelper(request, self.institution)

        expected = self.get_basic_total_cart_price()
        res = cart.get_total_cart()
        self.assertEqual(expected, res)
