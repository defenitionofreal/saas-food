from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.company.models import Institution
from apps.order.services.cart_helper import CartHelper


class SelectPaymentTypeAPIView(APIView):

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        payment_type = str(request.data["type"]).lower()
        if payment_type in [i.type for i in institution.payment_type.all()]:
            cart = CartHelper(request, institution)
            return cart.add_payment_type(payment_type)
        return Response({"detail": "Select a valid payment type"},
                        status=status.HTTP_400_BAD_REQUEST)
