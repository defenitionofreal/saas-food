from apps.delivery.models.enums import SaleType
from apps.order.models import PromoCode, Cart, CartItem
from apps.order.services.cart_helper import CartHelper
from apps.order.services.math_utils import get_absolute_from_percent_and_total
from apps.order.services.product_obj_to_cart_item_dict import get_cart_item_dict_from_product
from apps.order.tests.dummy_request import DummyRequest
from apps.order.tests.test_cart_setup import TestSetupBase


class TestCart(TestSetupBase):
    product1_price = 1000

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_products()

    @classmethod
    def create_products(cls):
        cls.prod1 = cls.create_simple_product(title='prod1', price=cls.product1_price, slug='p1')

    def get_cart(self, promo_code: PromoCode, product_quantity: int = 1) -> Cart:
        cart = Cart.objects.create(institution=self.institution, min_amount=self.get_cart_min_amount())
        prod1_dict = get_cart_item_dict_from_product(self.prod1)
        cart_item1 = CartItem.objects.create(cart=cart, product=prod1_dict, quantity=product_quantity)
        cart.items.set([cart_item1])
        cart.promo_code = promo_code
        cart.save()
        return cart

    def test_get_sale_absolute(self):
        """ Sale equals to initially defined value when product with category or id; else 0"""

        sale = 100
        promo_code = self.create_promo_code(sale=sale, code_type=SaleType.ABSOLUTE)
        product_category = self.prod1.category
        product_id = self.prod1.id

        request = DummyRequest(user=self.anon_user, generate_cart_id=True)
        db_cart = self.get_cart(promo_code=promo_code, product_quantity=1)
        db_cart.session_id = request.get_cart_session_id()
        db_cart.save()
        cart = CartHelper(request, self.institution)

        #### test nothing in category and product
        self.assertEqual(cart.get_sale, 0)

        #### test only category

        promo_code.categories.set([product_category])
        promo_code.save()

        # product quantity one
        self.assertEqual(cart.get_sale, sale)

        cart_item: CartItem = db_cart.items.all()[0]
        cart_item.quantity = 5
        cart_item.save()

        # product quantity few
        self.assertEqual(cart.get_sale, sale)

        #### test only product id

        promo_code.categories.set([])
        promo_code.products.set([product_id])
        promo_code.save()

        # product quantity few
        self.assertEqual(cart.get_sale, sale)

        cart_item: CartItem = db_cart.items.all()[0]
        cart_item.quantity = 1
        cart_item.save()

        # product quantity one
        self.assertEqual(cart.get_sale, sale)

    def test_get_sale_percent(self):
        sale = 50
        few_quantity = 5
        total_cart_quantity_one = self.product1_price
        total_cart_few_quantity = self.product1_price * few_quantity
        sale_quantity_few = get_absolute_from_percent_and_total(sale, total_cart_few_quantity)

        promo_code = self.create_promo_code(sale=sale, code_type=SaleType.PERCENT)
        product_category = self.prod1.category
        product_id = self.prod1.id

        request = DummyRequest(user=self.anon_user, generate_cart_id=True)
        db_cart = self.get_cart(promo_code=promo_code, product_quantity=1)
        db_cart.session_id = request.get_cart_session_id()
        db_cart.save()
        cart = CartHelper(request, self.institution)

        #### test nothing in category and product

        total_cart_nothing = self.product1_price
        sale_nothing = get_absolute_from_percent_and_total(sale, total_cart_nothing)
        self.assertEqual(cart.get_sale, sale_nothing)

        #### test only category

        promo_code.categories.set([product_category])
        promo_code.save()

        # category quantity one
        sale_cat_quantity_one = get_absolute_from_percent_and_total(sale, total_cart_quantity_one)
        self.assertEqual(cart.get_sale, sale_cat_quantity_one)

        # category few quantity
        cart_item: CartItem = db_cart.items.all()[0]
        cart_item.quantity = few_quantity
        cart_item.save()

        self.assertEqual(cart.get_sale, sale_quantity_few)

        #### test only product id

        promo_code.categories.set([])
        promo_code.products.set([product_id])
        promo_code.save()

        # product few quantity
        self.assertEqual(cart.get_sale, sale_quantity_few)

        cart_item: CartItem = db_cart.items.all()[0]
        cart_item.quantity = 1
        cart_item.save()

        # product quantity one
        self.assertEqual(cart.get_sale, sale_cat_quantity_one)
