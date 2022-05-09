from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.serializers import DesignSerializer
from apps.company.models import Design


class DesignDetailAPIView(APIView):
    """
    Retrieve, update or delete a design instance.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, design_pk):
        design = get_object_or_404(Design.objects, institution_id=pk, pk=design_pk)
        serializer = DesignSerializer(design)
        return Response(serializer.data)

    def put(self, request, pk, design_pk):
        design = get_object_or_404(Design.objects, institution_id=pk, pk=design_pk)
        serializer = DesignSerializer(design, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, design_pk):
        design = get_object_or_404(Design.objects,
                                   user=self.request.user,
                                   pk=design_pk)
        design.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
