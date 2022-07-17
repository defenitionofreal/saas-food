from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from apps.product.models import Product
from apps.company.models import Institution

from apps.order.services.cart_helper import CartHelper


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

        # check if request data exists
        if "title" not in request.data:
            title = product.title
        else:
            title = request.data['title']

        if "slug" not in request.data:
            slug = product.slug
        else:
            slug = request.data['slug']

        if "price" not in request.data:
            price = int(product.price)
        else:
            price = request.data['price']

        if "modifiers" not in request.data:
            modifiers = {}
        else:
            modifiers = request.data['modifiers']

        if "additives" not in request.data:
            additives = []
        else:
            additives = request.data['additives']

        # check if request data is relevant
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

        # new array for a product field
        product_dict = {
            "id": product.id,
            "category": product.category.slug,
            "title": title,
            "slug": slug,
            "price": price,
            "modifiers": modifiers,
            "additives": additives
        }

        cart = CartHelper(request=request,
                          institution=institution)
        return cart.add_item(product_dict)
