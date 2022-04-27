from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.product.models import Additive
from apps.product.serializers import AdditiveSerializer


class AdditiveListAPIView(APIView):
    """ List Additive """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Additive.objects.filter(user=self.request.user)
        serializer = AdditiveSerializer(query, many=True)
        return Response(serializer.data)
