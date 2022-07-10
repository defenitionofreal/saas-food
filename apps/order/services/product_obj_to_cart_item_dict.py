from apps.product.models import Product
from apps.product.models.cart_item_product_keys import *


def get_cart_item_dict_from_product_object_no_modifiers_no_additives(product: Product):
    if product:
        return {
            cart_item_prod_id: product.id,
            cart_item_prod_category: product.category.slug,
            cart_item_prod_title: product.title,
            cart_item_prod_slug: product.slug,
            cart_item_prod_price: product.price,
            cart_item_prod_modifiers: {},
            cart_item_prod_additives: []
        }
    return {}
