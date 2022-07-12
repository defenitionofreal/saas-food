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

        if user.is_authenticated:
            return self.__retrieve_cart_auth()
        else:
            return self.__retrieve_cart_not_auth()

    def __retrieve_cart_auth(self):
        institution = self.__get_institution()
        user = self.__get_user()
        cart = None
        fail_response = None

        # todo: maybe firstly check for cart session id and provide this if absent
        if self.has_cart_session_id:
            cart_session_id = self.__get_cart_session_id()
            return self.__retrieve_cart_auth_with_session_id(institution, user, cart_session_id)
        else:
            self.__add_cart_id_to_session()
            cart_session_id = self.__get_cart_session_id()
            cart = Cart.objects.filter(institution=institution, session_id=cart_session_id, customer=user).first()
            if not cart:
                fail_response = Response({"detail": "Cart does not exist. (auth cart)"})

        self.fail_response = fail_response
        self.cart = cart

    def __retrieve_cart_auth_with_session_id(self, institution: Institution, user, cart_session_id):
        cart = None
        fail_response = None
        cart = Cart.objects.filter(institution=institution, session_id=cart_session_id).first()
        if cart:
            if not cart.customer:
                cart.customer = user
                cart.save()
            # cart, cart_created = Cart.objects.get_or_create(
            #     institution=institution, customer=user)
            #
            # for session_item in session_cart.items.all():
            #     session_item.cart = cart
            #     session_item.save()
            #
            #     cart_item_duplicates = cart.items.filter(product__slug=session_item.product["slug"])
            #     if cart_item_duplicates.exists():
            #         for i in cart_item_duplicates:
            #             i.quantity = F("quantity") + session_item.quantity
            #             i.save(update_fields=("quantity",))
            #     else:
            #         cart.items.add(session_item)
            #         cart.save()
            #
            # if session_cart.promo_code:
            #     cart.promo_code = session_cart.promo_code
            #     cart.save()
            #
            # session_cart.delete()
            # del session[settings.CART_SESSION_ID]
            # #session.flush()
        else:
            # if no session cart
            cart, cart_created = Cart.objects.get_or_create(institution=institution, customer=user,
                                                            session_id=cart_session_id)

        self.fail_response = fail_response
        self.cart = cart

    def __retrieve_cart_auth_no_session_id(self, institution: Institution, user):
        cart = None
        fail_response = None
        self.__add_cart_id_to_session()
        cart_session_id = self.__get_cart_session_id()
        cart = Cart.objects.filter(institution=institution, session_id=cart_session_id, customer=user).first()
        if not cart:
            fail_response = Response({"detail": "Cart does not exist. (auth cart)"})

        self.fail_response = fail_response
        self.cart = cart

    def __retrieve_cart_not_auth(self):
        if self.has_cart_session_id:
            self.cart = Cart.objects.get(institution=self.__get_institution(), session_id=self.__get_cart_session_id())
        else:
            self.fail_response = Response({"detail": "Cart does not exist. (session cart)"})
