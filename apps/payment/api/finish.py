from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import Cart

from apps.payment.models.enums.payment_type import PaymentType
from apps.payment.models.enums.payment_status import PaymentStatus
from apps.payment.models import Payment
from apps.payment.services.YooMoney.auth_url import YooMoneyAuth


CLIENT_ID = "A5E16040AAE558A718B74B72B3E1BA7880B71AD7310D5A306B6E13A115295B39"
SECRET_ID = "A8E57BA73BB226CCDBF1FC4757178AB5F15223CECEA544AE034C261FCB540A74FDA5D1FE68CC7744D231F3188033FFBFD408CD466AF51B27967D0899E748F883"
REDIRECT_URL = "http://api.scaneat.ru"
SCOPE = ["account-info",
         "operation-history",
         "operation-details",
         "incoming-transfers"]

# TODO: (yoomoney) пока беспонтовая вьюшка
class FinishPaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # def get(self):
    #     ya_auth = YooMoneyAuth(CLIENT_ID, SECRET_ID, REDIRECT_URL, SCOPE)

    def get(self, request):
        #institution = Institution.objects.get(domain=domain)
        # order_obj = request.query_params["orderId"]
        # gateway = request.query_params["gateway"]

        return Response({"detail": "successful payment"})

    # def post(self, request, domain):
    #     institution = Institution.objects.get(domain=domain)
    #     order_obj = request.query_params["orderId"]
    #     # gateway = request.query_params["gateway"] ?
    #
    #     payment = Payment.objects.filter(institution=institution,
    #                                      order_id=order_obj)
    #     if payment.exists():
    #         payment = payment.first()
    #
    #         # если оплата статус завершена -> заказ статус в процессе
    #
    #         return Response({"d": payment.status})
