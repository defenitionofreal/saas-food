def merge_two_carts(cart_to, cart_from):
    """ Combines carts together. cart_from is not changed """

    from apps.order.models import Cart
    if not isinstance(cart_to, Cart) or not isinstance(cart_from, Cart):
        return
