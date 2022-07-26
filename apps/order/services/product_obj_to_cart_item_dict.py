from apps.product.models import Product
from apps.order.models.cart_item import CartItemProductKeys as pkeys


def get_cart_item_dict_from_product(product: Product,
                                    modifiers: dict = None,
                                    additives: list = None):
    if product:
        modifiers = modifiers if modifiers else {}
        additives = additives if additives else []
        return {
            pkeys.id: product.id,
            pkeys.category: product.category.slug,
            pkeys.title: product.title,
            pkeys.slug: product.slug,
            pkeys.price: product.price,
            pkeys.modifiers: modifiers,
            pkeys.additives: additives
        }
    return {}
