import hashlib
import json

item = {"qty": 1,
        "price": 250,
        "additives": [{"title": "cheese", "price": 15},
                      {"title": "red souce", "price": 10}],
        "modifiers": [{"title": "25 cm", "price": 200}]
        }

# using encode() + dumps() to convert to bytes
dict_to_bytes = json.dumps(item).encode('utf-8')

m = hashlib.md5()
m.update(dict_to_bytes)

def to_representation(self, instance):
    """
    """
    rep = super(self, self).to_representation(instance)
    session = self.context["request"].session

    for item in instance.items.all():
        #check = item.check_if_product_in_session(session)
        products = session.get("product_with_options")
        if products:
            if item.product.slug in products["product"].keys():
                price = products["product"][item.product.slug]["price"]
                additives_total = products["product"][item.product.slug]["additives_price"]
                if "additives" in products["product"][item.product.slug]:
                    additives = [v for k, v in products["product"][item.product.slug]["additives"].items()
                                 if products["product"][item.product.slug]["additives"]]
                else:
                    additives = []
                if "modifiers" in products["product"][item.product.slug]:
                    modifiers = [v for v in products["product"][item.product.slug]["modifiers"].values()
                                 if products["product"][item.product.slug]["modifiers"]]
                else:
                    modifiers = []
                # выводит только 1 товар !!!
                item_response = {item.product.slug: {"price": price,
                                                     "additives_total": additives_total,
                                                     "additives": additives,
                                                     "modifiers": modifiers}}
                rep['items'] = item_response
                rep['get_total_cart'] = (int(rep['items'][item.product.slug]["price"]) + int(rep['items'][item.product.slug]["additives_total"]))
            else:
                pass
                # update with products that not in session?
                # print(rep['items'])
                # rep['items'].update({i.product.slug: {"price": i.product.price}
                #             for i in instance.items.all()})
        else:
            rep['items'] = {i.product.slug: {"price": i.product.price}
                            for i in instance.items.all()}
    return rep
