from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Order
from apps.order.serializers import OrderSerializer


class CheckoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        session = self.request.session
        user = self.request.user

        name = request.data['name']
        phone = request.data['phone']
        comment = request.data['comment']
        payment_type = request.data['payment_type']

        if payment_type in institution.payment_type.values_list("type",
                                                                flat=True):
            payment_type = institution.payment_type.get(type=payment_type)
        else:
            return Response({"detail": "Wrong payment type"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.is_authenticated:
            # cart check
            cart = Cart.objects.filter(institution=institution,
                                       customer=user)
            # if settings.CART_SESSION_ID in session:
            #     cart = Cart.objects.filter(institution=institution,
            #                                customer=user,
            #                                session_id=session[
            #                                    settings.CART_SESSION_ID])
            if cart.exists():
                cart = cart.first()

                order, created = Order.objects.update_or_create(
                    institution=institution, customer=user, cart=cart,
                    defaults={"name": name,
                              "phone": phone,
                              "comment": comment,
                              "payment_type": payment_type.type})

                serializer = OrderSerializer(order)

            return Response({"detail": serializer.data})
        else:
            return Response({"detail": "Please login"})
