from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.que.models import Que

from apps.order.models import Cart
from apps.order.models.enums import OrderStatus
from apps.order.services.generate_order_number import generate_order_number

from apps.payment.models.enums.payment_type import PaymentType
from apps.payment.models.enums.payment_status import PaymentStatus
from apps.payment.models import Payment
from apps.payment.services.stripe.helper import StripeClient

from django.db import transaction

# TODO: Пока не ясно как сделать так чтобы при вебхуках от платежных систем,
#  были использованы api ключи каждой отдельной организации.
#  Решение сейчас такое:
#  создать в ручную урлы для вебхука под каждого юзера, а от юзера брать ключ для запроса


class CheckoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user, session = self.request.user, self.request.session

        name = request.data['name']
        phone = request.data['phone']
        email = request.data['email']
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
        order.name = name if name else user.first_name
        order.phone = phone if phone else user.phone
        order.email = email if email else user.email
        order.comment = comment
        order.payment_type = payment_type
        if (order.code is None) or (order.code in ("", " ")):
            order.code = generate_order_number(order.institution_id)
        order.save()

        msg = {"status": "error",
               "status_code": 400,
               "message": "Order not placed",
               "url": None}

        with transaction.atomic():
            # payment create
            payment, _ = Payment.objects.update_or_create(order=order)

            if payment_type == PaymentType.CASH:
                order.status = OrderStatus.PLACED
                order.save()
                payment.status = PaymentStatus.PENDING
                payment.save()
                # send notifications
                msg = {"status": "success",
                       "status_code": 200,
                       "message": "Order placed",
                       "url": None}

            if payment_type == PaymentType.CARD:
                order.status = OrderStatus.PLACED
                order.save()
                payment.status = PaymentStatus.PENDING
                payment.save()
                # send notifications
                msg = {"status": "success",
                       "status_code": 200,
                       "message": "Order placed",
                       "url": None}

            if payment_type == PaymentType.ONLINE:
                # todo: STRIPE and more
                if gateway == "stripe":
                    institution_stripe = institution.user.stripe_integration.first()
                    items_list = []
                    for cart_item in order.items.all():
                        item_dict = {
                            "title": cart_item.item.title,
                            "price": cart_item.get_item_price,
                            "quantity": cart_item.quantity,
                            "description": f"{cart_item.modifier.modifier.title if cart_item.modifier else ''}"
                                           f"{cart_item.additives.values_list('title', flat=True)}"
                             }
                        items_list.append(item_dict)

                    stripe = StripeClient(
                        host="http://localhost:8000",  # todo: self host!
                        api_key=institution_stripe.api_key
                    )
                    msg = stripe.create_checkout_session(
                        mode="payment",
                        customer_email=email,
                        line_items=items_list,
                        order_id=str(order.id)
                    )

                if gateway == "yoomoney":
                    pass

                # не нужно при онлайн оплате ставить статус placed так как
                # если не оплатит и вернуться, то корзина не должна пропасть
                payment.status = PaymentStatus.PENDING
                payment.save()
                # todo: send notifications

        return Response(msg)

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
