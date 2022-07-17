# core
from django.conf import settings
from django.db.models import F
# apps
from apps.order.services.generate_cart_key import _generate_cart_key
from apps.order.models import Cart, CartItem
# rest framework
from rest_framework.response import Response
# other


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

    def _cart_get_or_create(self) -> tuple:
        """ get or create cart """
        self._check_or_generate_session_cart_id_key()
        if self._is_user_auth():
            cart, cart_created = Cart.objects.get_or_create(
                institution=self.institution,
                customer=self.user,
                session_id=self.session[settings.CART_SESSION_ID])
        else:
            cart, cart_created = Cart.objects.get_or_create(
                institution=self.institution,
                session_id=self.session[settings.CART_SESSION_ID])
        return cart, cart_created

    # ======= CONDITIONS & DEDUCTIONS =======
    # todo: здесь написать методы, которые разгрузят модель Cart

    def get_total_cart(self):
        pass

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
