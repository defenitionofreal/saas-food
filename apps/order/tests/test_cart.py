from apps.delivery.models.enums import SaleType
from apps.order.services.product_obj_to_cart_item_dict import \
    get_cart_item_dict_from_product_object_no_modifiers_no_additives
from apps.order.tests.test_setup_base import TestSetupBase
from apps.product.models.product import Product
from apps.order.models import Cart, CartItem


class TestCartNoModifiersAdditivesInProduct(TestSetupBase):
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
        cls.prod1 = Product.objects.create(category=cls.category, title='prod1', description='d',
                                           price=cls.product1_price,
                                           weight=1, cook_time=1, slug='p1')
        cls.prod2 = Product.objects.create(category=cls.category, title='prod2', description='d',
                                           price=cls.product2_price,
                                           weight=1, cook_time=1, slug='p2')

    @classmethod
    def create_cart(cls):
        cls.cart = Cart.objects.create(institution=cls.institution)
        prod1_dict = get_cart_item_dict_from_product_object_no_modifiers_no_additives(cls.prod1)
        prod2_dict = get_cart_item_dict_from_product_object_no_modifiers_no_additives(cls.prod2)

        cls.cart_item1 = CartItem.objects.create(cart=cls.cart, product=prod1_dict, quantity=cls.quantity_p1)
        cls.cart_item2 = CartItem.objects.create(cart=cls.cart, product=prod2_dict, quantity=cls.quantity_p2)

        cls.cart.items.set([cls.cart_item1, cls.cart_item2])

    def get_cart(self) -> Cart:
        return self.cart

    def get_basic_total_cart_price(self):
        return self.product1_price * self.quantity_p1 + self.product2_price * self.quantity_p2

    def test_get_total_cart(self):
        expected = self.get_basic_total_cart_price()
        res = self.get_cart().get_total_cart
        self.assertEqual(expected, res)

    def test_final_price_with_delivery_and_bonus(self):
        delivery_sale = 25
        delivery_sale_type = SaleType.ABSOLUTE
        cart = self.get_cart()
        delivery = self.create_delivery_obj(delivery_sale, delivery_sale_type)
        delivery_info = self.create_delivery_info_obj(delivery)
        cart.delivery = delivery_info

        customer_bonus = 30
        cart.bonus = self.create_bonus(is_promo_code=True)
        cart.customer_bonus = customer_bonus

        expected_final_price = self.get_basic_total_cart_price() - (delivery_sale + customer_bonus)
        result_final_price = cart.final_price

        self.assertEqual(expected_final_price, result_final_price)
        cart.delivery = None
