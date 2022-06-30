from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Order
from apps.order.serializers import OrderSerializer
from apps.payment.models.enums.payment_type import PaymentType
from apps.payment.models.enums.payment_status import PaymentStatus
from apps.payment.models import Payment

from django.conf import settings


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
            payment_type = institution.payment_type.get(type=payment_type).type
        else:
            return Response({"detail": "Wrong payment type"},
                            status=status.HTTP_400_BAD_REQUEST)

        # cart check
        cart = Cart.objects.filter(institution=institution,
                                   customer=user,
                                   session_id=session[
                                       settings.CART_SESSION_ID])
        if cart.exists():
            cart = cart.first()

            # order create or update
            order, order_created = Order.objects.update_or_create(
                institution=institution,
                customer=user,
                cart=cart,
                session_id=cart.session_id,
                defaults={"name": name,
                          "phone": phone,
                          "comment": comment,
                          "payment_type": payment_type})

            # payment create or update
            payment, payment_created = Payment.objects.update_or_create(
                institution=institution,
                user=user,
                order=order,
                defaults={"total": order.final_price})

            # check if payment type is online by card
            if payment_type == PaymentType.ONLINE:
                # check for gateway param
                if "gateway" not in request.data:
                    return Response({"detail": "Choose your payment gateway"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    gateway = request.data['gateway']

                payment.type = PaymentType.ONLINE
                payment.status = PaymentStatus.PENDING
                payment.save()

                # if customer choose pay by yoomoney
                if gateway == "yoomoney":
                    wallet = institution.user.yoomoney.\
                        values_list("wallet", flat=True)[0]
                    if wallet:
                        from apps.payment.services.YooMoney.send_payment import YooMoneyPay
                        client = YooMoneyPay(receiver=wallet,
                                             quickpay_form="shop",
                                             targets=f"Заказ {order.id}",
                                             paymentType="AC",
                                             sum=2,  #order.final_price  #TODO: change
                                             formcomment=f"Заказ {order.id}",
                                             shortdest=f"Заказ {order.id}",
                                             label=order.id,
                                             successURL=f"http://localhost:8000/api/showcase/{institution.domain}/menu/")  #TODO: host change
                        return Response(
                            {"redirected_url": client.redirected_url})
            # if another PaymentType

        if user.is_authenticated:
            pass
            # cart check
            # cart = Cart.objects.filter(institution=institution,
            #                            customer=user)
            # # if settings.CART_SESSION_ID in session:
            # #     cart = Cart.objects.filter(institution=institution,
            # #                                customer=user,
            # #                                session_id=session[
            # #                                    settings.CART_SESSION_ID])
            # if cart.exists():
            #     cart = cart.first()
            #
            #     order, created = Order.objects.update_or_create(
            #         institution=institution, customer=user, cart=cart,
            #         defaults={"name": name,
            #                   "phone": phone,
            #                   "comment": comment,
            #                   "payment_type": payment_type.type})
            #
            #     serializer = OrderSerializer(order)
            #
            # return Response({"detail": serializer.data})
        else:
            return Response({"detail": "Please login"})
