from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Order
from apps.order.models.enums import OrderStatus
from apps.order.services.cart_helper import CartHelper
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

        name = request.data['name']
        phone = request.data['phone']
        comment = request.data['comment']
        payment_type = request.data['payment_type']
        gateway = request.data['gateway']

        order = Cart.objects.filter(institution=institution,
                                    customer=user,
                                    status=OrderStatus.DRAFT).first()

        if not order:
            return Response({"detail": "Create cart"},
                            status=status.HTTP_400_BAD_REQUEST)

        if order.payment_type is None:
            return Response({"detail": "Select payment type"},
                            status=status.HTTP_400_BAD_REQUEST)

        if order.delivery is None:
            return Response({"detail": "Add delivery information"},
                            status=status.HTTP_400_BAD_REQUEST)

        if payment_type not in institution.payment_type.values_list("type",
                                                                    flat=True):
            return Response({"detail": "Wrong payment type"},
                            status=status.HTTP_400_BAD_REQUEST)
        payment_type = institution.payment_type.get(type=payment_type).type

        # change order values
        order.name = name
        order.phone = phone
        order.comment = comment
        order.payment_type = payment_type
        order.save()

        # payment create
        payment, payment_created = Payment.objects.update_or_create(
            institution=institution,
            user=user,
            order=order,
            defaults={"total": order.final_price})

        if payment_type == PaymentType.CASH:
            order.status = OrderStatus.PLACED
            order.save()
            payment.status = PaymentStatus.PENDING
            payment.save()

        if payment_type == PaymentType.CARD:
            order.status = OrderStatus.PLACED
            order.save()
            payment.status = PaymentStatus.PENDING
            payment.save()

        if payment_type == PaymentType.ONLINE:
            order.status = OrderStatus.PLACED
            order.save()
            payment.status = PaymentStatus.PENDING
            payment.save()

        return Response({})

            # # if customer choose pay by yoomoney
            # if gateway == "yoomoney":
            #     wallet = institution.user.yoomoney.values_list("wallet", flat=True)[0]
            #     if wallet:
            #         from apps.payment.services.YooMoney.send_payment import YooMoneyPay
            #         client = YooMoneyPay(receiver=wallet,
            #                              quickpay_form="shop",
            #                              targets=f"Заказ {order.id}",
            #                              paymentType="AC",
            #                              sum=2,  #order.final_price  #TODO: change
            #                              formcomment=f"Заказ {order.id}",
            #                              shortdest=f"Заказ {order.id}",
            #                              label=order.id,
            #                              successURL=f"http://localhost:8000/api/showcase/{institution.domain}/menu/")  #TODO: host change
            #         del session[settings.CART_SESSION_ID] # удаляю ключ cart_id чтобы убрать корзину на стороне покупателя
            #         return Response({"redirected_url": client.redirected_url})
