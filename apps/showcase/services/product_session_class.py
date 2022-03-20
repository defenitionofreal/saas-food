class ProductSessionClass:
    def __init__(self, session, key: str):
        self.session = session
        self.key = key
        self.product_with_options = self.session.get(self.key)

    def check_product_with_options_obj(self):
        if not self.product_with_options:
            self.product_with_options = self.session[
                'product_with_options'] = {}
        self.product_with_options = self.product_with_options
        return self.product_with_options

    def check_product_obj(self, product):
        if not "product" in self.product_with_options:
            self.product_with_options["product"] = {
                product.slug: {"title": product.title,
                               "price": int(product.price),
                               "additives_price": 0}}
        return self.product_with_options["product"]

    def check_product_slug_obj(self, product):
        if not str(product.slug) in self.product_with_options["product"].keys():
            self.product_with_options["product"].update({
                product.slug: {"title": product.title,
                               "price": int(product.price),
                               "additives_price": 0}})
        return self.product_with_options["product"][product.slug]

    def check_product_stickers(self, product):
        product_sticker = [i for i in product.sticker.filter(
            is_active=True).order_by("id")]
        if product_sticker:
            self.product_with_options["product"][product.slug]["stickers"] = {
                sticker.id: {"title": sticker.title,
                             "bg_color": sticker.color,
                             "text_color": sticker.text_color}
                for sticker in product_sticker}
        else:
            self.product_with_options["product"][product.slug]["stickers"] = {}
        return self.product_with_options["product"][product.slug]["stickers"]

    def product_dict(self):
        return self.product_with_options["product"]

    def del_product_in_session(self):
        del self.product_with_options

    def del_session(self):
        return self.session.flush()
