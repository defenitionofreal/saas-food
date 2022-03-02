import random


def _generate_cart_key():
    """ function for generating random cart key values """
    cart_key = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_key += characters[random.randint(0, len(characters) - 1)]
    return cart_key

# DOWN: IT IS A SESSION CART LOGIC IN CUSTOM SERIALIZER
# cart = session.get(settings.CART_SESSION_ID)
# if not cart:
#     cart = session[settings.CART_SESSION_ID] = {}
# cart = cart
# print(session.session_key)
# product_id = str(product.id)
# if product_id in cart:
#     cart[product_id]['quantity'] += 1
#     session.modified = True
#     return Response({"detail": "Product quantity updated"})
# else:
#     cart[product_id] = {'title': product.title,
#                         'price': int(product.price),
#                         'quantity': 1}
#     session.modified = True
#     return Response({"detail": "New product added"})


# cart_items = session.get(settings.CART_SESSION_ID)
# if not cart_items:
#     cart_items = session[settings.CART_SESSION_ID] = {}
# # print(session.session_key)
#
# def get_single_item_total(item):
#     """ Sum price depending on quantity value """
#     total = item['price'] * item['quantity']
#     return total
#
# def get_total_cart():
#     """ Count total cart price """
#     total = 0
#     for i in cart_items.values():
#         total += get_single_item_total(i)
#     return total
#
# def get_bonus_accrual():
#     """  Accrual bonus points to a customer """
#     bonus = Bonus.objects.get(institution=institution)
#     if bonus.is_active:
#         if bonus.is_promo_code is True:
#             # total_accrual = round((bonus.accrual / Decimal(
#             #     '100')) * self.get_total_cart_after_sale)
#             pass
#         else:
#             total_accrual = round((bonus.accrual / Decimal('100')) * get_total_cart())
#         return total_accrual
#
# return Response({
#      "institution": {'domain': institution.domain},
#      #"created_at": datetime.datetime.now(),
#      "items": cart_items,
#      "total_cart": get_total_cart(),
#      "bonus_accrual": get_bonus_accrual(),
#      "promo_code": None,
#      })