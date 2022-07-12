from apps.order.models import Cart


def merge_two_carts(cart_to: Cart, cart_from: Cart):
    """ Combines carts together. cart_from is not changed """

    if not isinstance(cart_to, Cart) or not isinstance(cart_from, Cart):
        return
