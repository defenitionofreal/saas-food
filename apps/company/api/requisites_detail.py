from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.serializers import RequisitesSerializer
from apps.company.models import Requisites


class RequisitesDetailAPIView(APIView):
    """
    Retrieve, update or delete requisites.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, requisites_pk):
        query = get_object_or_404(Requisites.objects, institution_id=pk, pk=requisites_pk)
        serializer = RequisitesSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, requisites_pk):
        query = get_object_or_404(Requisites.objects, institution_id=pk, pk=requisites_pk)
        serializer = RequisitesSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, requisites_pk):
        query = get_object_or_404(Requisites.objects, institution_id=pk, pk=requisites_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
