from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.company.models import Institution
from apps.payment.services.stripe.helper import StripeClient


class StripeWebHookAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        owner_api_key = institution.user.stripe_integration.first().api_key
        try:
            stripe = StripeClient(
                host="http://localhost:8000",  # todo: self host!
                api_key=owner_api_key
            )
            stripe.webhook(request)
            return Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"{e}"},
                            status=status.HTTP_400_BAD_REQUEST)
