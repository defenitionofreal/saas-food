from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.product.serializers import StickerSerializer
from apps.company.models import Institution


class StickerCreateAPIView(APIView):
    """ Create new sticker """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = StickerSerializer(data=request.data)
        institution = Institution.objects.get(pk=pk)
        if serializer.is_valid():
            serializer.save(institution=institution)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
