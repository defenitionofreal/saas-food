from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem
from apps.order.services.generate_cart_key import _generate_cart_key

from django.conf import settings
from django.db.models import F

import hashlib
import json


class AddToCartAPIView(APIView):
    """
    Add product to cart view:
    - required requested array
    - get or create cart_id in sessions
    - check requested array data with data from db
    - creating md5 hash for a cart item
    - add or update an item in session cart
     DB stuff:
     - if auth get or create cart tied to a user
     - if not auth get or create cart tied to a session id
     - bottom logic check products, counts quantity, adds to cart
    """

    def post(self, request, domain, product_slug):

        institution = Institution.objects.get(domain=domain)
        product = get_object_or_404(Product, slug=product_slug)
        user = self.request.user

        # данные запроса в переменные
        title = request.data['title']
        slug = request.data['slug']
        modifiers = request.data['modifiers']
        additives = request.data['additives']
        price = request.data['price']
        total_price = request.data['total_price']

        # здесь я беру cart_id или создаю cart_id в сессии
        session = self.request.session
        if not settings.CART_SESSION_ID in session:
            session[settings.CART_SESSION_ID] = _generate_cart_key()
        else:
            session[settings.CART_SESSION_ID]
        cart_session = session

        # перепроверить подлинность данных с фронта
        if title != product.title:
            title = product.title
        if slug != product.slug:
            slug = product.slug
        if price != int(product.price):
            price = int(product.price)

        checked_additives_sum = 0
        if additives:
            for additive in additives:
                for i in product.additives \
                        .values("category_additive__title",
                                "category_additive__price") \
                        .filter(is_active=True, institution=institution):
                    if additive["title"] == i["category_additive__title"] and \
                       additive["price"] != int(i["category_additive__price"]):
                        additive["price"] = int(i["category_additive__price"])
                    checked_additives_sum += additive["price"]

        if modifiers:
            for i in product.modifiers \
                    .values("title", "modifiers_price__price") \
                    .filter(institution=institution):
                if modifiers["title"] == i["title"] and \
                   modifiers["price"] != int(i["modifiers_price__price"]):
                    modifiers["price"] = int(i["modifiers_price__price"])

        checked_total_price = price + checked_additives_sum
        if modifiers:
            checked_total_price = checked_additives_sum + modifiers["price"]

        if total_price != checked_total_price:
            total_price = checked_total_price

        # создаю массив для сессии из данных запроса
        product_dict = {
            "title": title,
            "slug": slug,
            "price": price,
            "quantity": 1,
            "modifiers": modifiers,
            "additives": additives,
            "total_price": total_price
        }

        # создаю уникальный хеш ключ данных массива для CartItem
        dict_to_bytes = json.dumps(product_dict).encode('utf-8')
        m = hashlib.md5()
        m.update(dict_to_bytes)
        product_key = m.hexdigest()

        if cart_session:
            if not "products" in cart_session:
                cart_session["products"] = {}

            if product_key in cart_session["products"].keys():
                cart_session["products"][product_key]["quantity"] += 1
            else:
                cart_session["products"][product_key] = product_dict
            session.modified = True

            # логика связанная с БД
            if user.is_authenticated:
                cart, cart_created = Cart.objects.get_or_create(
                    institution=institution, customer=user)
                cart_item, cart_item_created = CartItem.objects.get_or_create(
                    product_key=product_key, cart=cart)
            else:
                cart, cart_created = Cart.objects.get_or_create(
                    institution=institution,
                    session_id=session[settings.CART_SESSION_ID])
                cart_item, cart_item_created = CartItem.objects.get_or_create(
                    product_key=product_key, cart=cart)

            if cart_created is False:
                if cart.items.filter(product_key=product_key).exists():
                    cart_item.quantity = F("quantity") + 1
                    cart_item.save(update_fields=("quantity",))
                    return Response({"detail": "Product quantity updated"})
                else:
                    cart.items.add(cart_item)
                    return Response({"detail": "New product added"})
            else:
                cart.items.add(cart_item)
                return Response({"detail": "Cart created and product added"})
