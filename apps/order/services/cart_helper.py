# core
from django.db.models import F
from django.shortcuts import get_object_or_404

# apps
from apps.delivery.models import DeliveryInfo
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
from typing import Optional

import json
import hashlib


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

    def _get_user_delivery_info(self):
        if self.request.user.is_authenticated:
            delivery_info = DeliveryInfo.objects.filter(user=self.request.user)
        else:
            delivery_info = DeliveryInfo.objects.filter(
                session_id=self.request.session.session_key
            )
        if delivery_info.exists():
            delivery_info = delivery_info.first()
        else:
            delivery_info = None

        return delivery_info

    def _cart_get_or_create(self) -> tuple:
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
        # todo: remake delivery info
        # if self._get_user_delivery_info():
        #     cart.delivery = self._get_user_delivery_info()
        #     cart.save()

        return cart, created

    def _get_product_additives(self, product: Product, additives_req) -> list:
        """
        If req is not empty, check that additives exists and related to product
        """
        additives_list = []

        if additives_req:
            additives_qs = Additive.objects.filter(
                is_active=True,
                institutions=self.institution,
                category__is_active=True,
                category__product_additives__id=product.id
            ).only("id", "title")

            additives_req_map = {
                str(additive['title']).lower(): idx
                for idx, additive in enumerate(additives_req, 1)
            }

            additives_list = [additive
                              for additive in additives_qs
                              if additives_req_map.get(additive.title.lower())]

        return additives_list

    def _get_product_modifier(self, product: Product, modifiers_req) -> Optional[ModifierPrice]:
        """
        Takes product object and modifiers data from body via POST request.
        If data from request is equal to products modifier relation then
        :return modifier_price.
        """
        if modifiers_req:
            product_modifiers = product.modifiers.filter(
                institutions=self.institution,
                modifiers_price__product_id=product.id
            ).only("id", "title")

            for modifier in product_modifiers:
                if modifiers_req["title"].lower() == modifier.title.lower():
                    return modifier.modifiers_price.first()

    @staticmethod
    def _get_cart_item_hash(**kwargs):
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

    @staticmethod
    def merge_cart_items(order_user: Cart = None, order_session: Cart = None):
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

    # ======= ACTIONS =======
    def add_item(self):
        """ add new item to cart or update quantity of an item """
        cart, cart_created = self._cart_get_or_create()

        product_slug = self.request.data.get("product_slug", None)
        modifier_req = self.request.data.get("modifier", None)
        additives_req = self.request.data.get("additives", [])

        product = get_object_or_404(
            Product, slug=product_slug, institutions=self.institution
        )

        modifier_price = self._get_product_modifier(product, modifier_req)
        additives_list = self._get_product_additives(product, additives_req)
        # todo: проверить одинаковый товар с разных пользователей и разных корзин
        #  так как хеш теперь не учитывает cart_id!
        item_hash = self._get_cart_item_hash(
            item_id=product.id,
            modifier_id=modifier_price,
            additive_ids=additives_list
        )
        existing_cart_item = cart.products_cart.filter(item_hash=item_hash).first()
        if existing_cart_item:
            existing_cart_item.quantity = F("quantity") + 1
            existing_cart_item.save(update_fields=["quantity"])
        else:
            cart_item, cart_item_created = CartItem.objects.get_or_create(
                item=product,
                modifier=modifier_price,
                cart=cart,
                item_hash=item_hash
            )
            cart_item.additives.add(*additives_list)
            cart_item.save()

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
                    user_cart, _ = self._cart_get_or_create()

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
        coupon = CouponHelper(code, cart, self.request.user)
        return coupon.main()

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
