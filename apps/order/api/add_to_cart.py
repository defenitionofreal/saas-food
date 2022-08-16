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
        cart = CartHelper(request, institution)
        product_dict = cart.form_product_dict(product.slug)
        return cart.add_item(product_dict)
