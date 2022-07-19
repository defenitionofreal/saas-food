# core
from decimal import Decimal

from django.conf import settings
from django.db.models import F
# apps
from apps.order.services.generate_cart_key import _generate_cart_key
from apps.order.models import Cart, CartItem
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
        # what else ?

    # ======= BASIC METHODS =======
    # todo: здесь базовые методы, которые так или иначе часто необходимы

    def _has_cart_session_id(self):
        return settings.CART_SESSION_ID in self.session

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

    def _cart_get_or_create(self) -> tuple:
        """ get or create cart """
        self._check_or_generate_session_cart_id_key()
        if self._is_user_auth():
            cart, cart_created = Cart.objects.get_or_create(
                institution=self.institution,
                customer=self.user,
                session_id=self.session[settings.CART_SESSION_ID],
                min_amount=self._cart_min_amount())
        else:
            cart, cart_created = Cart.objects.get_or_create(
                institution=self.institution,
                session_id=self.session[settings.CART_SESSION_ID],
                min_amount=self._cart_min_amount())
        return cart, cart_created

    def _get_cart_if_exists(self):
        if not self._has_cart_session_id():
            return

        if self._is_user_auth():
            query = Cart.objects.filter(institution=self.institution,
                                        customer=self.user,
                                        session_id=self.session[settings.CART_SESSION_ID])
        else:
            query = Cart.objects.filter(institution=self.institution,
                                        session_id=self.session[settings.CART_SESSION_ID])

        return query.first()

    def _get_institution_bonus(self):
        return self.institution.bonuses.first()

    def _get_delivery(self):
        cart = self._get_cart_if_exists()
        if cart:
            return cart.delivery

    # ======= CONDITIONS & DEDUCTIONS =======
    # todo: здесь написать методы, которые разгрузят модель Cart

    def get_total_cart(self):
        cart = self._get_cart_if_exists()
        if cart:
            items = cart.items.all()
            return sum(i.get_total_item_price for i in items)
        return 0

    @property
    def get_total_cart_after_sale(self):
        total_cart = self.get_total_cart()
        basic_sale = self.get_sale
        customer_bonus_sale = self.get_customer_bonus_contribution_to_sale()
        total_sale = basic_sale + customer_bonus_sale
        return total_cart - total_sale

    @property
    def get_delivery_price(self):
        delivery = self._get_delivery()
        if delivery:
            return delivery.get_delivery_price()

    @property
    def get_free_delivery_amount(self):
        delivery = self._get_delivery()
        if delivery:
            return delivery.get_free_delivery_amount()

    @property
    def get_min_delivery_order_amount(self):
        delivery = self._get_delivery()
        if delivery:
            return delivery.get_min_delivery_order_amount()

    def get_customer_bonus_contribution_to_sale(self):
        """ How much customer bonus adds to basic discount, value >= 0"""
        cart = self._get_cart_if_exists()
        if cart:
            customer_bonus = cart.customer_bonus
            if customer_bonus:
                bonus = self._get_institution_bonus()
                if bonus and customer_bonus:
                    is_active = bonus.is_active
                    is_promo_code = bonus.is_promo_code
                    if is_active and is_promo_code:
                        return customer_bonus
        return 0

    @property
    def get_sale(self):
        """ Basic sale amount, value >= 0"""
        # todo: this method is too big for refactoring now, but is required for other stuf
        # i will implement this later
        return 0

    @property
    def get_bonus_accrual(self):
        """ How much bonus amount customer will get, value >= 0 """
        bonus = self._get_institution_bonus()
        if bonus and bonus.is_active:
            if bonus.is_promo_code:
                full_sum = self.get_total_cart_after_sale
            else:
                full_sum = self.get_total_cart()
            return get_absolute_from_percent_and_total(bonus.accrual, full_sum)
        return 0

    # ======= ACTIONS =======
    # todo: здесь методы действий покупателя

    def add_item(self, product_dict) -> Response:
        """ add new item to cart or update quantity of an item """
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

    def remove_item(self):
        """ remove item from cart """
        pass

    def get_cart(self):
        """ cart detail """
        pass
