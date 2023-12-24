# core
import os

from django.db.models import F
from django.shortcuts import get_object_or_404

# apps
from apps.order.models import Cart, CartItem
from apps.order.models.enums import OrderStatus
from apps.order.services.coupon_helper import CouponHelper
from apps.order.services.bonus_helper import BonusHelper
from apps.product.models.modifiers_price import ModifierPrice
from apps.product.models.additive import Additive
from apps.product.models import Product
# rest framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
# other
from typing import Optional, List

import json
import hashlib
import hmac


class CartHelper:
    """
    Main cart class with all needed funcs and counts
    """

    def __init__(self, request, institution):
        self.request = request
        self.institution = institution

    # ======= BASIC METHODS =======
    def _cart_min_amount(self) -> int:
        """ cart minimum amount rule """
        value = self.institution.min_cart_cost.values_list("cost", flat=True)
        if value:
            return value[0]
        return 0

    def cart_get_or_create(self) -> tuple:
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                institution=self.institution,
                status=OrderStatus.DRAFT,
                customer_id=self.request.user.id
                )

            if self.request.user.phone and not cart.phone:
                cart.phone = self.request.user.phone
                cart.save()
            if self.request.user.email and not cart.email:
                cart.email = self.request.user.email
                cart.save()
            # todo: main address if not address at cart
            # if self.user.addresslink_set.all().first():
            #     print("user.addresslink.first()", self.user.addresslink_set.all().first())
            #     pass
        else:
            cart, created = Cart.objects.get_or_create(
                institution=self.institution,
                status=OrderStatus.DRAFT,
                session_id=self.request.session.session_key
            )

        return cart, created

    def _get_product_additives(self, product_id: int, additives_ids: List[int]) -> list:
        """
        If req is not empty, check that additives exists and related to product
        """
        additives_qs = Additive.objects.filter(
            is_active=True,
            institutions=self.institution,
            category__is_active=True,
            category__product_additives__id=product_id
        ).values("id")

        return list(additives_qs.filter(id__in=additives_ids))

    def _get_product_modifier_price(self, product: Product, modifier_id) -> Optional[ModifierPrice]:
        """
        Takes product object and modifiers data from body via POST request.
        If data from request is equal to products modifier relation then
        :return modifier_price.
        """
        if not modifier_id:
            return

        product_modifiers = product.modifiers.filter(
            institutions=self.institution,
            modifiers_price__product_id=product.id
        ).only("id", "title")

        for modifier in product_modifiers:
            if modifier_id == modifier.id:
                # todo: at future multiple modifiers possible.
                return modifier.modifiers_price.first()

    @staticmethod
    def _get_cart_item_hash(**kwargs) -> str:
        """
        Generate unique cart item hash to check if item with that parameters
        already exists. It helps to add new product or update quantity.
        """
        fields = {
            key: value.id if key == "modifier_price" and value else
            value if key == "product_id" else
            [additive["id"] for additive in value] if key == "additive_ids" else
            value
            for key, value in kwargs.items()
        }
        product_fields_json = json.dumps(fields, sort_keys=True)
        secret_key = os.environ.get("SECURE_SALT")
        item_hash = hmac.new(
            secret_key.encode('utf-8'),
            product_fields_json.encode('utf-8'),
            hashlib.sha256).hexdigest()
        return item_hash

    @classmethod
    def merge_cart_items(cls, order_user: Cart = None, order_session: Cart = None):
        """ Merge guest session cart with auth user cart """
        guest_items = order_session.products_cart.all()
        user_items = order_user.products_cart.all()

        for guest_item in guest_items:
            item_duplicates = user_items.filter(item_hash=guest_item.item_hash)
            if item_duplicates.exists():
                for i in item_duplicates:
                    i.quantity = F("quantity") + guest_item.quantity
                    i.save(update_fields=("quantity",))
            else:
                guest_item.cart = order_user
                guest_item.save()

        if order_session.promo_code and not order_user.promo_code:
            order_user.promo_code = order_session.promo_code
            order_user.save()

        order_session.delete()

    def get_product_or_404(self, product_id: int) -> Optional[Product]:
        return get_object_or_404(Product, id=product_id, institutions=self.institution)

    # ======= ACTIONS =======
    def add_item(self):
        """ add new item to cart or update quantity of an item """
        cart, cart_created = self.cart_get_or_create()

        product_id = self.request.data.get("product", None)
        modifier_id = self.request.data.get("modifier", None)
        additives_ids = self.request.data.get("additives", [])

        product = self.get_product_or_404(product_id)

        modifier_price = self._get_product_modifier_price(product, modifier_id)
        additives = self._get_product_additives(product.id, additives_ids)

        item_hash = self._get_cart_item_hash(
            product_id=product.id,
            modifier_price=modifier_price,
            additive_ids=additives
        )

        cart_item, created = CartItem.objects.update_or_create(
            cart_id=cart.id,
            item_hash=item_hash,
            item_id=product.id,
            modifier_id=modifier_price.id if modifier_price else None
        )
        if not created:
            CartItem.objects.filter(id=cart_item.id).update(
                quantity=F("quantity") + 1)
        else:
            additive_ids = list(map(lambda additive: additive["id"], additives))
            cart_item.additives.set(additive_ids)

    def remove_item(self, item_hash: str):
        cart = self.get_cart()
        cart_item = cart.products_cart.filter(item_hash=item_hash).first()
        if not cart_item:
            raise ValidationError({"detail": "Product not in a cart."})

        if cart_item.quantity > 1:
            cart_item.quantity = F("quantity") - 1
            cart_item.save(update_fields=("quantity",))
        else:
            cart_item.delete()

    def get_cart(self) -> Cart:
        """ Cart Detail View """
        cart = None
        user_cart = None
        session_cart = None

        if self.request.user.is_authenticated:
            user_cart = Cart.objects.filter(
                institution=self.institution,
                customer_id=self.request.user.id,
                status=OrderStatus.DRAFT
            ).first()

            if self.request.session.session_key:
                session_cart = Cart.objects.filter(
                    institution=self.institution,
                    session_id=self.request.session.session_key,
                    status=OrderStatus.DRAFT
                ).first()

            if session_cart:
                if not user_cart:
                    user_cart, _ = self.cart_get_or_create()
                self.merge_cart_items(user_cart, session_cart)

            cart = user_cart
        else:
            if self.request.session.session_key:
                session_cart = Cart.objects.filter(
                    institution=self.institution,
                    session_id=self.request.session.session_key,
                    status=OrderStatus.DRAFT
                ).first()
                cart = session_cart

        return cart

    def add_coupon(self, code) -> Response:
        cart = self.get_cart()
        coupon = CouponHelper(code, cart)
        return coupon.main(user=self.request.user)

    def add_bonuses(self, amount: int):
        cart = self.get_cart()
        bonus = BonusHelper(amount, cart, self.request.user)
        return bonus.main()

    def add_payment_type(self, payment_type):
        cart = self.get_cart()
        cart.payment_type = payment_type
        cart.save()
        return Response({"detail": f"{payment_type} selected"},
                        status=status.HTTP_201_CREATED)

    def checkout(self):
        pass
