from apps.order.services.coupon_helper import CouponHelper


def get_promo_code_sale(cart) -> int:
    if cart.promo_code and cart.customer:
        helper = CouponHelper(cart.promo_code, cart)
        return helper.final_sale()[0]
    return 0
