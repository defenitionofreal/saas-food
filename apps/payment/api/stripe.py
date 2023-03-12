from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.company.models import Institution
from apps.order.models import Cart

from apps.payment.models.enums.payment_type import PaymentType
from apps.payment.models.enums.payment_status import PaymentStatus
from apps.payment.models import Payment
from apps.payment.services.YooMoney.auth_url import YooMoneyAuth
from apps.payment.services.stripe.helper import StripeClient


class StripeWebHookAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        pass

    def post(self, request, domain):
        pass
