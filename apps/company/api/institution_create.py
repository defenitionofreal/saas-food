from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.company.serializers import InstitutionSerializer


class InstitutionCreateAPIView(APIView):
    """ Create new institution """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
