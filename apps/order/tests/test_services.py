from apps.order.services.product_obj_to_cart_item_dict import \
    get_cart_item_dict_from_product_object_no_modifiers_no_additives
from apps.order.tests.test_setup_base import TestSetupBase
from apps.product.models import Product
from apps.product.models.cart_item_product_keys import *


class TestProductDBToDictConversion(TestSetupBase):

    def test_db_product_to_cart_item_dict_no_modifiers(self):
        title = 'prod1'
        price = 100
        slug = 'sl1'
        category = self.category.slug

        product = Product.objects.create(category=self.category, title=title, description='d', price=price,
                                      weight=1, cook_time=1, slug=slug)
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
