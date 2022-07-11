from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.order.api.cart_from_request import get_or_create_cart_from_request
from apps.order.serializers import CartSerializer
from apps.product.models import Product
from apps.company.models import Institution
from apps.order.services.generate_cart_key import _generate_cart_key

from django.conf import settings

from apps.product.models.cart_item_product_keys import *


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

        # check if request data exists
        if cart_item_prod_title not in request.data:
            title = product.title
        else:
            title = request.data[cart_item_prod_title]

        if cart_item_prod_slug not in request.data:
            slug = product.slug
        else:
            slug = request.data[cart_item_prod_slug]

        if cart_item_prod_price not in request.data:
            price = int(product.price)
        else:
            price = request.data[cart_item_prod_price]

        if cart_item_prod_modifiers not in request.data:
            modifiers = {}
        else:
            modifiers = request.data[cart_item_prod_modifiers]

        if cart_item_prod_additives not in request.data:
            additives = []
        else:
            additives = request.data[cart_item_prod_additives]

        # check if request data is relevant
        if title != product.title:
            title = product.title
        if slug != product.slug:
            slug = product.slug
        if price != int(product.price):
            price = int(product.price)

        # здесь я беру cart_id или создаю cart_id в сессии
        session = self.request.session
        if settings.CART_SESSION_ID not in session:
            session[settings.CART_SESSION_ID] = _generate_cart_key()

        session.modified = True
        cart_session = session

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

        # new dict for a product field
        product_dict = {
            cart_item_prod_id: product.id,
            cart_item_prod_category: product.category.slug,
            cart_item_prod_title: title,
            cart_item_prod_slug: slug,
            cart_item_prod_price: price,
            cart_item_prod_modifiers: modifiers,
            cart_item_prod_additives: additives
        }

        assert cart_session

        cart, cart_created = get_or_create_cart_from_request(request, domain)
        cart.add_product_to_cart(product_dict)

        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)
