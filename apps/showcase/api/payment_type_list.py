from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.payment.models import PaymentTypeInstitution
from apps.payment.serializers import PaymentTypeInstitutionSerializer


class PaymentTypeClientListAPIView(APIView):
    """
    List of payments types that acceptable for a customer from affiliate
    """

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = PaymentTypeInstitution.objects.filter(
            institution=institution
        )
        serializer = PaymentTypeInstitutionSerializer(query, many=True)
        return Response(serializer.data)
