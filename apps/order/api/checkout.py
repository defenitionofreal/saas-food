from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Order
from apps.order.serializers import OrderSerializer
from apps.payment.models.enums.payment_type import PaymentType

#TODO: если тип оплаты онлайн, то проверка и шлюз платежный
class CheckoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        session = self.request.session
        user = self.request.user

        # check if request data exists
        if "name" not in request.data:
            return Response({"detail": "Enter your name"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            name = request.data['name']

        if "phone" not in request.data:
            return Response({"detail": "Enter your phone"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            phone = request.data['phone']

        if "comment" not in request.data:
            comment = ""
        else:
            comment = request.data['comment']

        if "payment_type" not in request.data:
            return Response({"detail": "Choose your payment_type"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            payment_type = request.data['payment_type']

        # check if payment_type exists in db with affiliate
        if payment_type in institution.payment_type.values_list("type",
                                                                flat=True):
            payment_type = institution.payment_type.get(type=payment_type)
        else:
            return Response({"detail": "Wrong payment type"},
                            status=status.HTTP_400_BAD_REQUEST)

        # првоерить если оплата онлайн тут !!
        if payment_type == PaymentType.ONLINE:
            pass

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
