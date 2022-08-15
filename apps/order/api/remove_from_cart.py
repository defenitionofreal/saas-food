from rest_framework.views import APIView
from apps.company.models import Institution
from apps.order.services.cart_helper import CartHelper


class RemoveFromCartAPIView(APIView):
    """
    Remove product from cart
    - if auth look for a cart tied to a user
    - if not auth look for a cart tied to a session cart id
    - bottom logic looks for a product and rm it
    """

    def post(self, request, domain, product_id):
        institution = Institution.objects.get(domain=domain)
        cart = CartHelper(request, institution)
        return cart.remove_item(product_id)
