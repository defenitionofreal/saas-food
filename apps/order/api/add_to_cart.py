from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import Cart, CartItem
from apps.order.services.generate_cart_key import _generate_cart_key

from django.conf import settings
from django.db.models import F


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

        # здесь я беру cart_id или создаю cart_id в сессии
        session = self.request.session
        if not settings.CART_SESSION_ID in session:
            session[settings.CART_SESSION_ID] = _generate_cart_key()
        else:
            session[settings.CART_SESSION_ID]
        session.modified = True
        cart_session = session

        # перепроверить подлинность данных с фронта
        if title != product.title:
            title = product.title
        if slug != product.slug:
            slug = product.slug
        if price != int(product.price):
            price = int(product.price)

        # ==== check for additives ====
        product_additives = product.additives \
            .values("category_additive__title", "category_additive__price") \
            .filter(is_active=True, institution=institution,
                    category_additive__title__in=[additive['title']
                                                  for additive in additives]
                    ).order_by('category_additive__title')

        additives_map = {additive['title']: idx
                         for idx, additive in enumerate(additives)}

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
                additives.remove([additive for additive in additives
                                  if additive["title"] == i][0])

        # check if product dont have anu additives at all in DB
        if not product_additives and additives:
            additives = []

        # ==== check for modifiers ====
        product_modifiers = product.modifiers \
            .values("title", "modifiers_price__price",
                    "modifiers_price__product__slug") \
            .filter(institution=institution,
                    modifiers_price__product__slug=product.slug)
        if product_modifiers and modifiers:
            if modifiers["title"] == product_modifiers[0]["title"]:
                modifiers["price"] = int(product_modifiers[0]["modifiers_price__price"])
            else:
                modifiers.clear()
        if not product_modifiers and modifiers:
            modifiers.clear()

        # создаю массив для поля product в бд из данных запроса после проверки
        product_dict = {
            "id": product.id,
            "category": product.category.slug,
            "title": title,
            "slug": slug,
            "price": price,
            "modifiers": modifiers,
            "additives": additives
        }

        if cart_session:
            # логика связанная с БД
            if user.is_authenticated:
                cart, cart_created = Cart.objects.get_or_create(
                    institution=institution,
                    customer=user)
                cart_item, cart_item_created = CartItem.objects.get_or_create(
                    product=product_dict,
                    cart=cart)
            else:
                cart, cart_created = Cart.objects.get_or_create(
                    institution=institution,
                    session_id=session[settings.CART_SESSION_ID])
                cart_item, cart_item_created = CartItem.objects.get_or_create(
                    product=product_dict,
                    cart=cart)

            if cart_created is False:
                if cart.items.filter(product=product_dict).exists():
                    cart_item.quantity = F("quantity") + 1
                    cart_item.save(update_fields=("quantity",))
                    return Response({"detail": "Product quantity updated"})
                else:
                    cart.items.add(cart_item)
                    return Response({"detail": "New product added"})
            else:
                cart.items.add(cart_item)
                return Response({"detail": "Cart created and product added"})
