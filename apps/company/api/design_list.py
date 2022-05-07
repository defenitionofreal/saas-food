from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Design
from apps.company.serializers import DesignSerializer


class DesignListAPIView(APIView):
    """ List Designs """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Design.objects.filter(user=self.request.user)
        serializer = DesignSerializer(query, many=True)
        return Response(serializer.data)
