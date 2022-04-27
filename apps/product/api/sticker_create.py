from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.product.serializers import StickerSerializer
from apps.company.models import Institution
from apps.company.services.compare_institution import _find_wrong_inst_id


class StickerCreateAPIView(APIView):
    """ Create new sticker """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StickerSerializer(data=request.data)
        institution = Institution.objects.filter(user=self.request.user)
        if request.data["institution"]:
            if _find_wrong_inst_id(request.data["institution"],
                                   institution.values_list('id', flat=True)):
                return Response({"detail": f"wrong institution id"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "institution is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
