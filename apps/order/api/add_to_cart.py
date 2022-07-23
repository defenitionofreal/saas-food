from django.http import Http404
from rest_framework.views import APIView
from apps.company.models import Institution
from apps.order.services.cart_helper import CartHelper
from apps.product.product_to_dict_serializers import ProductDictSerializer


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
        serializer = ProductDictSerializer(request_data=self.request.data,
                                           product_slug=product_slug,
                                           institution=institution)
        if serializer.is_valid:
            cart = CartHelper(request=request,
                              institution=institution)
            return cart.add_item(serializer.as_dict)
        else:
            raise Http404
