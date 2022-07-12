from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution, MinCartCost
from apps.order.api.cart_retriever import CartRetriever
from apps.order.serializers import CartSerializer


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
        cart_cost = MinCartCost.objects.filter(institution=institution).first()

        cart_retriever = CartRetriever(request, domain)
        if not cart_retriever.has_cart:
            return cart_retriever.get_response()

        # always modify request because cart session id might be added
        self.request = cart_retriever.request
        cart = cart_retriever.get_cart()

        try:
            if cart_cost:
                cart.min_amount = cart_cost.cost
                cart.save()

            if cart.items.exists():
                serializer = CartSerializer(cart, context={"request": self.request})
                return Response(serializer.data)
            else:
                return Response({"detail": "Cart is empty."})
        except Exception as e:
            return Response({"detail": f"{e}"})
