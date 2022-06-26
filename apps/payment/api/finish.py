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


# TODO: (yoomoney) пока беспонтовая вьюшка
class FinishPaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        order_obj = request.query_params["orderId"]
        # gateway = request.query_params["gateway"] ?

        payment = Payment.objects.filter(institution=institution,
                                         order_id=order_obj)
        if payment.exists():
            payment = payment.first()

            # если оплата статус завершена -> заказ статус в процессе

            return Response({"d": payment.status})
