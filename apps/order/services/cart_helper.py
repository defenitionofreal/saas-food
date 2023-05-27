# core
from django.conf import settings
from django.db.models import F
# apps
from apps.delivery.models import DeliveryInfo
from apps.order.services.generate_cart_key import _generate_cart_key
from apps.order.models import Cart, CartItem
from apps.order.models.enums import OrderStatus
from apps.order.serializers import CartSerializer
from apps.order.services.coupon_helper import CouponHelper
from apps.order.services.bonus_helper import BonusHelper
from apps.product.models.modifiers_price import ModifierPrice
from apps.product.models.additive import Additive
from apps.product.models import Product
# rest framework
from rest_framework.response import Response
from rest_framework import status
# other
from typing import Optional

import json
import hashlib


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
        value = self.institution.min_cart_cost.values_list("cost", flat=True)
        if value:
            return value[0]
        return 0

    def _get_user_delivery_info(self):
        if self._is_user_auth():
            delivery_info = DeliveryInfo.objects.filter(user=self.user)
        else:
            delivery_info = DeliveryInfo.objects.filter(
                session_id=self.session.session_key
            )
        if delivery_info.exists():
            delivery_info = delivery_info.first()
        else:
            delivery_info = None

        return delivery_info

    def _cart_get_or_create(self) -> tuple:
        """ get or create cart """
        self._check_or_generate_session_cart_id_key()
        if self._is_user_auth():
            cart, cart_created = Cart.objects.get_or_create(
                institution=self.institution,
                status=OrderStatus.DRAFT,
                customer_id=self.user.id,
                session_id=self.session[settings.CART_SESSION_ID],
                min_amount=self._cart_min_amount())

            if self.user.phone:
                cart.phone = self.user.phone
                cart.save()
            if self.user.email:
                cart.email = self.user.email
                cart.save()
            if self.user.addresslink_set.all().first():
                print("user.addresslink.first()", self.user.addresslink_set.all().first())
                pass
        else:
            cart, cart_created = Cart.objects.get_or_create(
                institution=self.institution,
                status=OrderStatus.DRAFT,
                session_id=self.session[settings.CART_SESSION_ID],
                min_amount=self._cart_min_amount())

        if self._get_user_delivery_info():
            cart.delivery = self._get_user_delivery_info()
            cart.save()

        return cart, cart_created

    def _get_product_additives(self, product, additives_req) -> list:
        """
        If req is not empty, check that additives exists and related to product
        """
        additives_list = []

        if additives_req:
            additives_qs = Additive.objects.filter(
                is_active=True,
                institution=self.institution,
                category__is_active=True,
                category__product_additives__id=product.id
            ).only("id", "title", "description", "image")

            additives_req_map = {str(additive['title']).lower(): idx
                                 for idx, additive in enumerate(additives_req)}

            for additive in additives_qs:
                idx = additives_req_map.get(additive.title.lower())
                if idx is not None:
                    additives_list.append(additive)

        return additives_list

    def _get_product_modifier(self, product, modifiers_req) -> Optional[ModifierPrice]:
        """
        Takes product object and modifiers data from body via POST request.
        If data from request is equal to products modifier relation then
        :return modifier_price.
        """
        if modifiers_req:
            product_modifiers = product.modifiers.filter(
                institution=self.institution,
                modifiers_price__product__slug=product.slug
            ).only("id", "title")

            for modifier in product_modifiers:
                if modifiers_req["title"].lower() == modifier.title.lower():
                    return modifier.modifiers_price.first()

    def _get_cart_item_hash(self, **kwargs):
        """
        Generate unique cart item hash to check if item with that parameters
        already exists at a cart.
        It helps to add new product or update quantity.
        """
        fields = {
            key: value.id
            if key == "modifier_id" and value else [i.id for i in value]
            if key == "additive_ids" and value else value
            for key, value in kwargs.items()
        }
        product_fields_json = json.dumps(fields, sort_keys=True)
        hash_obj = hashlib.sha256()
        hash_obj.update(product_fields_json.encode('utf-8'))
        item_hash = hash_obj.hexdigest()

        return item_hash

    # ======= CONDITIONS & DEDUCTIONS =======
    def get_total_cart(self):
        cart, _ = self._cart_get_or_create()
        items = cart.items.all()
        return sum(i.get_total_item_price for i in items)

    # ======= ACTIONS =======
    def add_item(self, product) -> Response:
        """ add new item to cart or update quantity of an item """

        cart, cart_created = self._cart_get_or_create()

        modifiers_req = self.request.data.get("modifiers", None)
        additives_req = self.request.data.get("additives", [])

        modifier_price = self._get_product_modifier(product, modifiers_req)
        additives_list = self._get_product_additives(product, additives_req)
        item_hash = self._get_cart_item_hash(cart_id=cart.id,
                                             item_id=product.id,
                                             modifier_id=modifier_price,
                                             additive_ids=additives_list)

        cart_item, cart_item_created = CartItem.objects.get_or_create(
            item=product,
            modifier=modifier_price,
            cart=cart,
            item_hash=item_hash
        )
        cart_item.additives.add(*additives_list)
        cart_item.save()

        if not cart_created:
            if cart.items.filter(item_hash=cart_item.item_hash).exists():
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
                    status=OrderStatus.DRAFT,
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
                cart = Cart.objects.filter(institution=self.institution,
                                           status=OrderStatus.DRAFT,
                                           session_id=self.session[
                                               settings.CART_SESSION_ID],
                                           customer_id=self.user.id).first()
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

    def add_bonuses(self, amount):
        cart, _ = self._cart_get_or_create()
        bonus = BonusHelper(amount, cart, self.user)
        return bonus.main()

    def add_payment_type(self, payment_type):
        cart, _ = self._cart_get_or_create()
        cart.payment_type = payment_type
        cart.save()
        return Response({"detail": f"{payment_type} selected"},
                        status=status.HTTP_201_CREATED)

    def checkout(self):
        pass
