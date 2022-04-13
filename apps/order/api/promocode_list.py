from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.order.models import PromoCode
from apps.order.serializers import PromoCodeSerializer


class PromoCodeListAPIView(APIView):
    """ List promo codes """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = PromoCode.objects.filter(institution=institution)
        serializer = PromoCodeSerializer(query, many=True)
        return Response(serializer.data)
