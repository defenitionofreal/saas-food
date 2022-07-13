from apps.order.models import Cart, CartItem
from apps.order.services.cart_merging import merge_two_carts
from apps.order.services.product_obj_to_cart_item_dict import \
    get_cart_item_dict_from_product_object_no_modifiers_no_additives
from apps.order.tests.test_setup_base import TestSetupBase
from apps.product.models.cart_item_product_keys import *


class TestProductDBToDictConversion(TestSetupBase):

    def test_db_product_to_cart_item_dict_no_modifiers(self):
        title = 'prod1'
        price = 100
        slug = 'sl1'
        category = self.category.slug

        product = self.make_simple_product(title, price, slug)

        expected_dict = {
            cart_item_prod_id: product.id,
            cart_item_prod_category: category,
            cart_item_prod_title: title,
            cart_item_prod_slug: slug,
            cart_item_prod_price: price,
            cart_item_prod_modifiers: {},
            cart_item_prod_additives: []
        }

        out_dict = get_cart_item_dict_from_product_object_no_modifiers_no_additives(product)

        self.assertDictEqual(expected_dict, out_dict)

    def test_cart_merging(self):
        title_1 = 'prod1'
        title_2 = 'prod2'
        price_1 = 100
        price_2 = 35
        slug_1 = 'sl1'
        slug_2 = 'sl2'
        q_prod_1_cart_1 = 2
        q_prod_2_cart_1 = 3
        q_prod_1_cart_2 = 4
        q_prod_2_cart_2 = 5

        product_1 = self.make_simple_product(title_1, price_1, slug_1)
        product_2 = self.make_simple_product(title_2, price_2, slug_2)

        cart1: Cart = Cart.objects.create(institution=self.institution)
        cart2: Cart = Cart.objects.create(institution=self.institution)
        prod1_dict = get_cart_item_dict_from_product_object_no_modifiers_no_additives(product_1)
        prod2_dict = get_cart_item_dict_from_product_object_no_modifiers_no_additives(product_2)

        cart1_item1 = CartItem.objects.create(cart=cart1, product=prod1_dict, quantity=q_prod_1_cart_1)
        cart1_item2 = CartItem.objects.create(cart=cart1, product=prod2_dict, quantity=q_prod_2_cart_1)
        cart1.items.set([cart1_item1, cart1_item2])

        cart2_item1 = CartItem.objects.create(cart=cart2, product=prod1_dict, quantity=q_prod_1_cart_2)
        cart2_item2 = CartItem.objects.create(cart=cart2, product=prod2_dict, quantity=q_prod_2_cart_2)
        cart2.items.set([cart2_item1, cart2_item2])

        expected_price = (q_prod_1_cart_1 + q_prod_1_cart_2) * price_1 + (q_prod_2_cart_1 + q_prod_2_cart_2) * price_2
        merge_two_carts(cart1, cart2)
        self.assertEqual(cart1.final_price, expected_price)
