from rest_framework.views import APIView
from rest_framework.response import Response
from apps.order.services.cart_helper import CartHelper
from apps.company.models import Institution

cart_item_id_key = 'cart_item_id'


class RemoveFromCartAPIView(APIView):
    """ Remove product from cart  """
    # TODO: странное решение передовать pk в body, а не в УРЛ.
    #  Так же из=за try/except если вообще ничего не передать, то будет этот ValueError
    #  недоработанно здесб с этим
    #  лучше по pk в урл и убрать try except, if else для обработки больше подойдет
    def post(self, request, domain):
        try:
            cart_item_id = None
            if cart_item_id_key in request.data:
                cart_item_id = int(request.data[cart_item_id_key])

            institution = Institution.objects.get(domain=domain)
            cart = CartHelper(request=request, institution=institution)
            return cart.remove_product_or_decrease_quantity_by_id(cart_item_id=cart_item_id)
        except ValueError:
            return Response({"detail": "This product not in a cart"})
