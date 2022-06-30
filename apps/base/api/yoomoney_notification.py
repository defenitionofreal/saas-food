from django.db import transaction
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.order.models import Cart, Order
from apps.order.models.enums.order_status import OrderStatus
from apps.order.serializers import OrderSerializer
from apps.payment.models.enums.payment_type import PaymentType
from apps.payment.models.enums.payment_status import PaymentStatus
from apps.payment.models import Payment

import dateutil.parser
import hashlib

# TODO: (yoomoney) секрет для уведомлений сделать полем в модели
YANDEX_MONEY_SECRET_WORD = "5j8lK2M4L5tp+iE0m9ppyb8E"


class YooMoneyHttpNotificationAPIView(APIView):

    def post(self, request):
        line_notification_options = '%s&%s&%s&%s&%s&%s&%s&%s&%s' % (
            request.POST['notification_type'],
            request.POST['operation_id'],
            request.POST['amount'],
            request.POST['currency'],
            request.POST['datetime'],
            request.POST['sender'],
            request.POST['codepro'],
            YANDEX_MONEY_SECRET_WORD,
            request.POST['label'])

        # for key, value in request.POST.items():
        #     print(f"{key}: {value}")

        if request.POST['sha1_hash'] ==\
                hashlib.sha1(line_notification_options.encode()).hexdigest():
            payment = Payment.objects.filter(order_id=request.POST["label"])
            if payment.exists():
                payment = payment[0]
                with transaction.atomic():
                    # if payment accepted
                    if request.POST["unaccepted"] is not True:
                        # payment part
                        payment.status = PaymentStatus.SUCCESS
                        payment.code = request.POST["operation_label"]
                        payment.save()
                        # order part
                        order = payment.order
                        order.status = OrderStatus.ACCEPTED
                        order.paid = True
                        order.save()
                        # del cart_id from session
                        session = self.request.session
                        del session[settings.CART_SESSION_ID]
                        # отправить нотификацию на почту/номер/телеграм (task)

            return Response({}, status=status.HTTP_200_OK)
        print("all bad")
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
