product_with_options = {
        "product": {
            "slug": "margarita",
            "title": "margarita",
            "price": 350,
            "total": 350,
            "additives": {
                1: {
                "title": "mozarella",
                "price": 30,
                "counter": 1},
                2: {
                "title": "margarita",
                "price": 20,
                "counter": 1}
            }
        }}

id = 3

if "additives" in product_with_options["product"]:
    if id in product_with_options["product"]["additives"].keys():
        product_with_options["product"]["additives"][id]["counter"] += 1
        product_with_options["product"]["total"] += product_with_options["product"]["additives"][id]["price"]
    else:
        product_with_options["product"]["additives"].update(
            {id: {'new': 'new'}})
else:
    product_with_options["product"]["additives"] = {id:{"new": "new"}}

print(product_with_options["product"])
