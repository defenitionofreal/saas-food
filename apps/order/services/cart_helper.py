# core
from django.conf import settings
from django.db.models import F
# apps
from apps.order.services.generate_cart_key import _generate_cart_key
from apps.order.models import Cart, CartItem
from apps.order.serializers import CartSerializer
from apps.order.services.coupon_helper import CouponHelper
from apps.product.models import Product
# rest framework
from rest_framework.response import Response
from rest_framework import status
# other


class CartHelper:
    """
    Main cart class with all needed funcs and counts
    """

    def __init__(self, request, institution):
        self.request = request
        self.user = request.user
        self.session = request.session
        self.institution = institution

    # ======= BASIC METHODS =======
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

    def _form_product_additives(self, product, additives) -> list:
        product_additives = product.additives \
            .values("category_additive__title", "category_additive__price") \
            .filter(is_active=True, institution=self.institution,
                    category_additive__title__in=[additive['title']
                                                  for additive in
                                                  additives]
                    ).order_by('category_additive__title')

        additives_map = {additive['title']: idx for idx, additive in
                         enumerate(additives)}

        # check for a additive in DB and set the right price from DB
        for i in product_additives:
            idx = additives_map.get(i['category_additive__title'])
            if idx is not None:
                additives[idx]["price"] = int(i["category_additive__price"])

        # check if request json has not wanted values and clean it if does
        difference = list(set(i["title"] for i in additives) -
                          set([i["category_additive__title"]
                               for i in product_additives]))
        if difference:
            for i in difference:
                additives.remove(
                    [additive for additive in additives
                     if additive["title"] == i][0])

        # check if product dont have any additives at all in DB
        if not product_additives and additives:
            additives = []

        return additives

    def _form_product_modifiers(self, product, modifiers) -> dict:
        product_modifiers = product.modifiers \
            .values("title", "modifiers_price__price",
                    "modifiers_price__product__slug") \
            .filter(institution=self.institution,
                    modifiers_price__product__slug=product.slug)
        if product_modifiers and modifiers:
            if not any(modifiers["title"] in mod["title"]
                       for mod in product_modifiers):
                modifiers.clear()
            else:
                for mod in product_modifiers:
                    if modifiers["title"] == mod["title"]:
                        modifiers["price"] = int(mod["modifiers_price__price"])
        else:
            modifiers.clear()

        return modifiers

    def form_product_dict(self, product_slug) -> dict:
        product = Product.objects.filter(slug=product_slug)
        if product.exists():
            product = product.first()
            product_dict = {
                "id": product.id,
                "category": product.category.slug,
                "title": product.title,
                "slug": product.slug,
                "price": int(product.price),
                "modifiers": self._form_product_modifiers(
                    product, self.request.data['modifiers'])
                    if "modifiers" in self.request.data else {},
                "additives": self._form_product_additives(
                    product, self.request.data['additives'])
                    if "additives" in self.request.data else []
            }
            return product_dict

    # ======= CONDITIONS & DEDUCTIONS =======
    def get_total_cart(self):
        cart, _ = self._cart_get_or_create()
        items = cart.items.all()
        return sum(i.get_total_item_price for i in items)

    # ======= ACTIONS =======
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
                                status=status.HTTP_201_CREATED)
            else:
                cart.items.add(cart_item)
                return Response({"detail": "New product added"},
                                status=status.HTTP_201_CREATED)
        else:
            cart.items.add(cart_item)
            return Response({"detail": "Cart created and product added"},
                            status=status.HTTP_201_CREATED)

    def remove_item(self, product_id) -> Response:
        """ remove item from cart """
        cart, cart_created = self._cart_get_or_create()

        if cart.items.filter(id=product_id).exists():
            cart_item = cart.items.get(id=product_id,
                                       cart=cart)
            if cart_item.quantity > 1:
                cart_item.quantity = F("quantity") - 1
                cart_item.save(update_fields=("quantity",))
            else:
                cart.items.remove(cart_item)
            return Response({"detail": "Product quantity updated"})
        else:
            return Response({"detail": "This product not in a cart"})

    def get_cart(self) -> Response:
        """ cart detail """
        if self._is_user_auth():
            if settings.CART_SESSION_ID in self.session:
                cart = Cart.objects.filter(
                    institution=self.institution,
                    session_id=self.session[settings.CART_SESSION_ID]).first()
                if cart and not cart.customer:
                    cart.customer = self.user
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
                    cart, cart_created = self._cart_get_or_create()
            else:
                self._check_or_generate_session_cart_id_key()
                cart = Cart.objects.filter(institution=self.institution,
                                           session_id=self.session[
                                               settings.CART_SESSION_ID],
                                           customer=self.user).first()
                if not cart:
                    return Response(
                        {"detail": "Cart does not exist. (auth cart)"},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            cart, cart_created = self._cart_get_or_create()

        if cart.items.exists():
            serializer = CartSerializer(cart,
                                        context={"request": self.request})
            return Response(serializer.data)
        else:
            return Response({"detail": "Cart is empty."})

    def add_coupon(self, code) -> Response:
        cart, _ = self._cart_get_or_create()
        coupon = CouponHelper(code, cart, self.user)
        return coupon.main()
