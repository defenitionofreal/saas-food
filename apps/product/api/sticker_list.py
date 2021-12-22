from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Institution
from apps.product.models import Sticker
from apps.product.serializers import StickerSerializer
from apps.base.authentication import JWTAuthentication


class StickerListAPIView(APIView):
    """ List stickers """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Sticker.objects.filter(institution=institution)
        serializer = StickerSerializer(query, many=True)
        return Response(serializer.data)
