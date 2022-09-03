def total_item_cart_price(item):
    """
    Count total item cart/order price
    with all modifiers, additives and quantity if they exists
    else basic item price
    """
    item_price = item["product__price"]

    if item["product__modifiers"]:
        item_price = item["product__modifiers"]["price"]

    if item["product__additives"]:
        for i in item["product__additives"]:
            item_price += i["price"]

    quantity = item["quantity"]
    total_price = (item_price * quantity)

    return int(total_price)
