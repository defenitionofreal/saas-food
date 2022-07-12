from apps.order.models import PromoCode
from apps.order.services.math_utils import get_absolute_from_percent_and_total

prod_category = 'product__category'
prod_slug = 'product__slug'
prod_price = 'product__price'
quantity = 'quantity'
slug = 'slug'


def cart_calculate_sale(cart):
    from apps.order.models import Cart
    if not isinstance(cart, Cart) or cart.promo_code is None:
        return 0

    promo_code: PromoCode = cart.promo_code
    sale = promo_code.sale

    items_cat = cart.items.values(prod_category, prod_slug, prod_price, quantity)
    items_prod = cart.items.values(prod_slug, prod_price, quantity)

    has_promo_code_categories = promo_code.categories.all()
    code_cat = []
    if has_promo_code_categories:
        code_cat = promo_code.categories.values_list(slug, flat=True)

    has_promo_code_products = cart.promo_code.products.all()
    code_product = []
    if has_promo_code_products:
        code_product = promo_code.products.values_list(slug, flat=True)

    # ABSOLUTE SALE
    if promo_code.is_absolute_sale:
        # categories participate coupon
        if has_promo_code_categories:
            for i in items_cat:
                if i[prod_category] in code_cat:
                    sale = sale
            sale = sale if sale >= 0.0 else 0.0
            return sale
        # products participate coupon
        if has_promo_code_products:
            for i in items_prod:
                if i[prod_slug] in code_product:
                    sale = sale
            sale = sale if sale >= 0.0 else 0.0
            return sale

        sale = sale if sale >= 0.0 else 0.0
        return sale

    # PERCENT SALE
    if promo_code.is_percent_sale:
        # categories participate coupon
        if has_promo_code_categories:
            cat_total = 0
            for i in items_cat:
                if i[prod_category] in code_cat:
                    cat_total += i[prod_price] * i[quantity]
            cat_total = cat_total if cat_total >= 0.0 else 0.0
            return get_absolute_from_percent_and_total(sale, cat_total)

        # products participate coupon
        if has_promo_code_products:
            products_total = 0
            for i in items_prod:
                if i[prod_slug] in code_product:
                    products_total += i[prod_price] * i[quantity]
            products_total = products_total if products_total >= 0.0 else 0.0
            return get_absolute_from_percent_and_total(sale, products_total)
        return get_absolute_from_percent_and_total(sale, cart.get_total_cart)
