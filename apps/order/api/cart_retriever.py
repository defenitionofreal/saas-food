from rest_framework.response import Response

from apps.company.models import Institution
from apps.order.models import Cart
from django.conf import settings

from apps.order.services.generate_cart_key import _generate_cart_key


class CartRetriever:
    """
    retrieves cart from session
    modifies request
    always override request in outer scope!
    """

    def __init__(self, request, domain):
        self.request = request
        self.domain = domain
        self.cart: Cart = None
        self.fail_response: Response = Response()
        self.__retrieve()

    @property
    def has_cart(self):
        return isinstance(self.cart, Cart)

    def get_cart(self):
        return self.cart

    def get_response(self):
        return self.fail_response

    def __add_cart_id_to_session(self):
        self.request.session[settings.CART_SESSION_ID] = _generate_cart_key()

    @property
    def has_cart_session_id(self):
        return settings.CART_SESSION_ID in self.request.session

    def __get_cart_session_id(self):
        if self.has_cart_session_id:
            return self.request.session[settings.CART_SESSION_ID]

    def __get_institution(self):
        return Institution.objects.get(domain=self.domain)

    def __get_user(self):
        return self.request.user

    def __retrieve(self):
        user = self.__get_user()

        if user and user.is_authenticated:
            return self.__retrieve_cart_auth()
        else:
            return self.__retrieve_cart_not_auth()

    def __retrieve_cart_auth(self):
        if self.has_cart_session_id:
            return self.__retrieve_cart_auth_with_session_id()
        else:
            return self.__retrieve_cart_auth_no_session_id()

    def __retrieve_cart_auth_with_session_id(self):
        institution = self.__get_institution()
        user = self.__get_user()
        cart_session_id = self.__get_cart_session_id()

        user_db_cart: Cart = Cart.objects.filter(institution=institution, customer=user).first()
        session_anon_cart: Cart = Cart.objects.filter(institution=institution,
                                                session_id=cart_session_id).exclude(customer=user).first()

        can_merge_carts = user_db_cart and session_anon_cart and (user_db_cart.id != session_anon_cart.id)
        if can_merge_carts:
            user_db_cart.merge_with_cart(session_anon_cart)
            self.cart = user_db_cart
            session_anon_cart.delete()
            return

        if user_db_cart:
            self.cart = user_db_cart
            return

        if session_anon_cart:
            session_anon_cart.customer = user
            session_anon_cart.save()
            self.cart = session_anon_cart
            return

        cart, cart_created = Cart.objects.get_or_create(institution=institution, customer=user,
                                                        session_id=cart_session_id)
        self.cart = cart

    def __retrieve_cart_auth_no_session_id(self):
        institution = self.__get_institution()
        user = self.__get_user()

        self.__add_cart_id_to_session()

        cart_session_id = self.__get_cart_session_id()
        self.cart = Cart.objects.filter(institution=institution, session_id=cart_session_id, customer=user).first()
        if not self.cart:
            self.fail_response = Response({"detail": "Cart does not exist. (auth cart)"})

    def __retrieve_cart_not_auth(self):
        cart_session_id = ''
        if self.has_cart_session_id:
            cart_session_id = self.__get_cart_session_id()

        # search for carts not assigned to customer (for privacy)
        self.cart = Cart.objects.filter(institution=self.__get_institution(), session_id=cart_session_id,
                                        customer=None).first()
        if self.cart is None:
            self.fail_response = Response({"detail": "Cart does not exist. (session cart)"})
