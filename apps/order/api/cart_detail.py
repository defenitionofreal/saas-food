from rest_framework.views import APIView
from apps.company.models import Institution
from apps.order.services.cart_helper import CartHelper


class CartAPIView(APIView):
    """
    Cart Detail View:
    - if auth than check for session
     - if session cart than create user cart and move items from one to another
     - if no session cart or session than check for user cart or create one
    - if not auth
     - check for session cart but if no cart than raise it
    """

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        cart = CartHelper(request, institution)
        return cart.get_cart()
