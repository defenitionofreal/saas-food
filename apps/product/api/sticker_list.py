from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.product.models import Sticker
from apps.product.serializers import StickerSerializer


class StickerListAPIView(APIView):
    """ List stickers """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Sticker.objects.filter(user=self.request.user)
        serializer = StickerSerializer(query, many=True)
        return Response(serializer.data)
