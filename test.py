import hashlib
import json

# item = {"qty": 1,
#         "price": 250,
#         "additives": [{"title": "cheese", "price": 15},
#                       {"title": "red souce", "price": 10}],
#         "modifiers": [{"title": "25 cm", "price": 200}]
#         }
#
#
# product_dict = {
#             "title": "title",
#             "slug": "slug",
#             "price": 100,
#             "quantity": 1,
#             "modifiers": None,
#             "additives": [],
#             "total_price": 222
#         }
#
# # using encode() + dumps() to convert to bytes
# dict_to_bytes = json.dumps(item).encode('utf-8')
# m = hashlib.md5()
# m.update(dict_to_bytes)

query1 = ["drinks"]
query2 = ["drinks", "pizza"]
if query2 in query1:
    print("yes")
else:
    print("no")
