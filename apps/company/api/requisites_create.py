from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.company.serializers import RequisitesSerializer
from apps.company.models import Institution


class RequisitesCreateAPIView(APIView):
    """ Create new requisites """
    permission_classes = [IsAuthenticated]

    # на фронте create or update
    def post(self, request, pk):
        serializer = RequisitesSerializer(data=request.data)
        institution = Institution.objects.get(pk=pk)
        if serializer.is_valid():
            serializer.save(institution=institution)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
