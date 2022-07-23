from apps.product.models import Product
from apps.order.models.cart_item import (CartItemProductKeys as product_keys,
                                         CartItemAdditiveKeys as additives_keys,
                                         CartItemModifierKeys as modifiers_keys)


class ProductDict:
    def __init__(self, product_id: int = -1, slug: str = '', category: str = '',
                 title: str = '', price: int = 0, modifiers=None, additives=None):
        self.product_id = product_id
        self.slug = slug
        self.category = category
        self.title = title
        self.price = price
        self.modifiers = modifiers
        self.additives = additives

        if not self.modifiers:
            self.modifiers = []
        if not self.additives:
            self.additives = {}

    def as_dict(self):
        return {
            product_keys.id: self.product_id,
            product_keys.category: self.category,
            product_keys.title: self.title,
            product_keys.slug: self.slug,
            product_keys.price: self.price,
            product_keys.modifiers: self.modifiers,
            product_keys.additives: self.additives
        }


class ProductDictSerializer:
    def __init__(self, request_data, product_slug, institution):
        self.request_data = request_data
        self.institution = institution
        self.product_slug = product_slug
        self.product = Product.objects.filter(slug=product_slug).first()
        self.product_dict = ProductDict()
        if self.product and self.institution:
            self.extract()

    @property
    def is_valid(self):
        return self.product is not None

    @property
    def as_dict(self):
        return self.product_dict.as_dict()

    def extract(self):
        self.product_dict.product_id = self.product.id
        self.product_dict.slug = self.product.slug
        self.product_dict.category = self.product.category.slug
        self.product_dict.title = self.product.title
        self.product_dict.price = int(self.product.price)
        self.extract_modifiers()
        self.extract_additives()

    def extract_modifiers(self):
        if product_keys.modifiers in self.request_data:
            modifiers = self.request_data[product_keys.modifiers]
            product_modifiers = self.product.modifiers \
                .values("title", "modifiers_price__price",
                        "modifiers_price__product__slug") \
                .filter(institution=self.institution,
                        modifiers_price__product__slug=self.product.slug)
            if product_modifiers and modifiers:
                if modifiers[modifiers_keys.title] == product_modifiers[0][modifiers_keys.title]:
                    modifiers[modifiers_keys.price] = int(product_modifiers[0]["modifiers_price__price"])
                else:
                    modifiers.clear()
            if not product_modifiers and modifiers:
                modifiers.clear()

            self.product_dict.modifiers = modifiers

    def extract_additives(self):
        if product_keys.additives in self.request_data:
            additives = self.request_data[product_keys.additives]
            additive_titles = [additive[additives_keys.title] for additive in additives]

            product_additives = self.product.additives \
                .values("category_additive__title", "category_additive__price") \
                .filter(is_active=True, institution=self.institution,
                        category_additive__title__in=additive_titles
                        ).order_by('category_additive__title')

            additives_map = {additive[additives_keys.title]: idx
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
                                      if additive[additives_keys.title] == i][0])

            # check if product dont have anu additives at all in DB
            if not product_additives and additives:
                additives = []

            self.product_dict.additives = additives
