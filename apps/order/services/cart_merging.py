def merge_two_carts(cart_to, cart_from):
    """ Combines carts together. cart_from is not changed """

    from apps.order.models import Cart
    if not isinstance(cart_to, Cart) or not isinstance(cart_from, Cart):
        return

    for item in cart_from.items.all():
        cart_to.add_or_merge_item_to_cart(item)

    new_promo_code = cart_from.promo_code
    if new_promo_code:
        cart_to.promo_code = new_promo_code
    cart_from.save()
