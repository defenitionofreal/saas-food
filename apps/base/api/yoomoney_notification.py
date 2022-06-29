from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart, Order
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

        for key, value in request.POST.items():
            print("changes here")
            print("key:", key)
            print("value:", value)

        if request.POST['sha1_hash'] == hashlib.sha1(line_notification_options.encode()).hexdigest():
            print("all good")
            return Response({"data": line_notification_options}, status=200)
        print("all bad")
        return Response({}, status=400)
