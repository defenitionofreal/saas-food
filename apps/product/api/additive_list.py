from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Additive
from apps.product.serializers import AdditiveSerializer
from apps.base.authentication import JWTAuthentication


class AdditiveListAPIView(APIView):
    """ List Additive """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Additive.objects.filter(institution=institution)
        serializer = AdditiveSerializer(query, many=True)
        return Response(serializer.data)
