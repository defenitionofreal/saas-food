# core
from django.conf import settings
from django.db.models import F
# apps
from apps.order.services.cart_access import cart_get_or_create
from apps.order.services.generate_cart_key import _generate_cart_key
from apps.order.models import CartItem
from apps.delivery.services.delivery_helper import DeliveryHelper
# rest framework
from rest_framework.response import Response

# other
from apps.order.services.math_utils import get_absolute_from_percent_and_total


class CartHelper:
    """
    Main cart class with all needed funcs and counts
    """

    def __init__(self, request, institution):
        self.user = request.user
        self.session = request.session
        self.institution = institution
        # cache cart when requested first time
        self.cart_cached = None
        # what else ?

    # ======= BASIC METHODS =======
    # todo: здесь базовые методы, которые так или иначе часто необходимы

    def _check_or_generate_session_cart_id_key(self):
        """ cart_id in sessions needed for all further requests """
        if settings.CART_SESSION_ID not in self.session:
            self.session[settings.CART_SESSION_ID] = _generate_cart_key()
        self.session.modified = True

    def _is_user_auth(self) -> bool:
        """ check if user is authenticated or not """
        if self.user.is_authenticated:
            return True
        return False

    def _cart_min_amount(self) -> int:
        """ cart minimum amount rule """
        value = self.institution.min_cart_value.values_list("cost", flat=True)
        if value:
            return value[0]
        return 0

    def refresh_cached_cart(self):
        """ Cache refresh is not necessary during  regular work, but useful for test purposes """
        self._cart_get_or_create(force_refresh_cache=True)

    def _cart_get_or_create(self, force_refresh_cache=False) -> tuple:
        """ get or create cart """
        if self.cart_cached and not force_refresh_cache:
            return self.cart_cached, False

        self._check_or_generate_session_cart_id_key()
        session_id = self.session[settings.CART_SESSION_ID]
        min_amount = self._cart_min_amount()

        cart, is_created = cart_get_or_create(session_id=session_id,
                                              min_amount=min_amount,
                                              institution=self.institution,
                                              user=self.user)
        self.cart_cached = cart
        return cart, is_created

    def get_cart_obj(self):
        """ Guaranteed to return a valid Cart  """
        return self._cart_get_or_create()[0]

    def _get_institution_bonus_obj(self):
        return self.institution.bonuses.first()

    def _get_promo_code(self):
        return self.get_cart_obj().promo_code

    def _get_customer_bonus_points(self) -> [int, None]:
        """ How much bonus points set up to this cart to get write off """
        return self.get_cart_obj().customer_bonus

    def _get_user_bonus_obj(self) -> [int, None]:
        if self._is_user_auth():
            return self.institution.user_bonuses.filter(user=self.user).first()

    def _get_delivery(self) -> [DeliveryHelper, None]:
        cart = self.get_cart_obj()
        delivery = cart.delivery
        if delivery:
            return DeliveryHelper(delivery)

    # ======= CONDITIONS & DEDUCTIONS =======
    # todo: здесь написать методы, которые разгрузят модель Cart

    @property
    def get_total_cart(self) -> int:
        cart = self.get_cart_obj()
        items = cart.items.all()
        return sum(i.get_total_item_price for i in items)

    @property
    def get_total_cart_after_sale(self) -> int:
        total_cart = self.get_total_cart
        coupon_sale = self.get_sale
        customer_bonus_sale = self.get_customer_bonus_contribution_to_sale()
        total_sale = coupon_sale + customer_bonus_sale
        return total_cart - total_sale

    @property
    def get_delivery_price(self) -> [int, None]:
        delivery = self._get_delivery()
        if delivery:
            return delivery.delivery_price

    @property
    def get_free_delivery_amount(self) -> [int, None]:
        delivery = self._get_delivery()
        if delivery:
            return delivery.free_delivery_amount

    @property
    def get_min_delivery_order_amount(self) -> [int, None]:
        delivery = self._get_delivery()
        if delivery:
            return delivery.min_delivery_order_amount

    @property
    def get_delivery_sale(self) -> [int, None]:
        delivery = self._get_delivery()
        if delivery:
            cart_total = self.get_total_cart_after_sale
            return delivery.get_delivery_sale(cart_total)

    @property
    def get_delivery_zone(self):
        delivery = self._get_delivery()
        if delivery:
            return delivery.get_delivery_zone

    @property
    def is_free_delivery_by_promo_code(self) -> bool:
        promo_code = self._get_promo_code()
        return promo_code and promo_code.delivery_free

    def calculate_final_delivery_price(self, cart_current_price) -> int:
        """ Final delivery expenses, value >= 0  """
        if self.is_free_delivery_by_promo_code:
            return 0

        delivery = self._get_delivery()
        if delivery:
            return delivery.calculate_final_delivery_price(cart_current_price)

        return 0

    def calculate_customer_bonus_write_off_for_final_price(self):
        """ Amount to remove from final price, value <= 0 """
        customer_bonus = self._get_customer_bonus_points()
        bonus = self._get_institution_bonus_obj()

        if None not in [customer_bonus, bonus]:
            if bonus.is_active and not bonus.is_promo_code:
                return -1 * customer_bonus
        return 0

    def get_customer_bonus_contribution_to_sale(self) -> int:
        """ How much customer bonus adds to basic discount, value >= 0"""
        customer_bonus = self._get_customer_bonus_points()
        if customer_bonus:
            bonus = self._get_institution_bonus_obj()
            if bonus:
                is_active = bonus.is_active
                is_promo_code = bonus.is_promo_code
                if is_active and is_promo_code:
                    return customer_bonus
        return 0

    @property
    def get_sale(self) -> int:
        """ Basic sale amount, value >= 0"""
        # todo: test and refactor this method
        promo_code = self._get_promo_code()
        cart = self.get_cart_obj()
        if promo_code:
            sale = promo_code.sale
            # if absolute sale type
            if promo_code.code_type == 'absolute':
                # categories participate coupon
                if promo_code.categories.all():
                    items_cat = cart.items.values("product__category",
                                                  "product__slug",
                                                  "product__price",
                                                  "quantity")
                    code_cat = promo_code.categories.values_list("slug",
                                                                 flat=True)
                    for i in items_cat:
                        if i["product__category"] in code_cat:
                            sale = sale
                    sale = sale if sale >= 0.0 else 0.0
                    return sale
                # products participate coupon
                if promo_code.products.all():
                    items = cart.items.values("product__slug",
                                              "product__price",
                                              "quantity")
                    code_product = promo_code.products.values_list("slug",
                                                                   flat=True)
                    for i in items:
                        if i["product__slug"] in code_product:
                            sale = sale
                    sale = sale if sale >= 0.0 else 0.0
                    return sale

                sale = sale if sale >= 0.0 else 0.0
                return sale

            # if percent sale type
            if promo_code.code_type == 'percent':

                # categories participate coupon
                if promo_code.categories.all():
                    cat_total = 0
                    items_cat = cart.items.values("product__category",
                                                  "product__slug",
                                                  "product__price",
                                                  "quantity")
                    code_cat = promo_code.categories.values_list("slug",
                                                                 flat=True)
                    for i in items_cat:
                        if i["product__category"] in code_cat:
                            cat_total += i["product__price"] * i["quantity"]
                    cat_total = cat_total if cat_total >= 0.0 else 0.0
                    return get_absolute_from_percent_and_total(sale, cat_total)

                # products participate coupon
                if promo_code.products.all():
                    products_total = 0
                    items = cart.items.values("product__slug",
                                              "product__price",
                                              "quantity")
                    code_product = promo_code.products.values_list("slug",
                                                                   flat=True)
                    for i in items:
                        if i["product__slug"] in code_product:
                            products_total += i["product__price"] * i[
                                "quantity"]
                    products_total = products_total if products_total >= 0.0 else 0.0
                    return get_absolute_from_percent_and_total(sale, products_total)
                return get_absolute_from_percent_and_total(sale, self.get_total_cart)
        return 0

    @property
    def get_bonus_accrual(self) -> int:
        """ How much bonus amount customer will get, value >= 0 """
        bonus = self._get_institution_bonus_obj()
        if bonus and bonus.is_active:
            if bonus.is_promo_code:
                full_sum = self.get_total_cart_after_sale
            else:
                full_sum = self.get_total_cart
            return get_absolute_from_percent_and_total(bonus.accrual, full_sum)
        return 0

    @property
    def final_price(self) -> int:
        price_after_sale = self.get_total_cart_after_sale
        customer_bonus_write_off = self.calculate_customer_bonus_write_off_for_final_price()
        delivery_price = self.calculate_final_delivery_price(price_after_sale)
        price_after_sale += customer_bonus_write_off + delivery_price

        return price_after_sale

    # ======= ACTIONS =======
    # todo: здесь методы действий покупателя

    def add_item(self, product_dict) -> Response:
        """ add new item to cart or update quantity of an item """

        """
        TODO: i've implemented this method in cart model because it is required
        we should better call this from there, because it is not big difference
        which text is returned in response since result is basically same
        """

        cart, cart_created = self._cart_get_or_create()
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            product=product_dict, cart=cart)

        if not cart_created:
            if cart.items.filter(product=product_dict).exists():
                cart_item.quantity = F("quantity") + 1
                cart_item.save(update_fields=("quantity",))
                return Response({"detail": "Product quantity updated"},
                                status=201)
            else:
                cart.items.add(cart_item)
                return Response({"detail": "New product added"},
                                status=201)
        else:
            cart.items.add(cart_item)
            return Response({"detail": "Cart created and product added"},
                            status=201)

    def add_customer_bonus(self, bonus_input: int) -> Response:
        """ Add customer bonus points to the cart """
        cart = self.get_cart_obj()
        customer_bonus_points = self._get_customer_bonus_points()
        bonus_obj = self._get_institution_bonus_obj()
        user_bonus_obj = self._get_user_bonus_obj()
        promo_code = self._get_promo_code()

        if customer_bonus_points is not None:
            return Response({"detail": "Bonuses already applied."})

        if not bonus_obj or bonus_obj.is_active is False:
            return Response({"detail": "Loyalty program is not active"})

        if not user_bonus_obj:
            return Response({"detail": "You dont have any bonuses yet."})

        user_bonus_amount_available = user_bonus_obj.bonus
        if bonus_input > user_bonus_amount_available:
            return Response({"detail": "Not enough bonuses."})

        bonus_write_off_percent = bonus_obj.write_off

        if promo_code is not None:
            if bonus_obj.is_promo_code is True:
                total_cart = cart.get_total_cart_after_sale
                sale = get_absolute_from_percent_and_total(bonus_write_off_percent, total_cart)
            else:
                return Response({"detail": "Use bonuses with promocode is not allowed."})
        else:
            total_cart = cart.get_total_cart
            sale = get_absolute_from_percent_and_total(bonus_write_off_percent, total_cart)

        if bonus_input > sale:
            return Response({"detail": f"Write off no more than {bonus_write_off_percent}% "
                                       f"of total price. ({sale} bonuses)"})
        cart.customer_bonus = bonus_input
        cart.save()
        user_bonus_obj.bonus -= bonus_input
        user_bonus_obj.save()
        return Response({"detail": f"{bonus_input} bonuses have been successfully redeemed"})

    def remove_item(self):
        """ remove item from cart """
        pass

    def get_cart(self):
        """ cart detail """
        # todo: remove?
        pass

    # ======= OTHER =======

    @property
    def is_not_empty(self):
        cart = self.get_cart_obj()
        return cart.items.exists()

    @property
    def is_empty(self):
        return not self.is_not_empty
