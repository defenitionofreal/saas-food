from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.serializers import WorkingHoursSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import WorkingHours


class WorkingHoursDetailAPIView(APIView):
    """
    Retrieve, update or delete a working hours.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, working_hours_pk):
        query = get_object_or_404(WorkingHours.objects, institution_id=pk, pk=working_hours_pk)
        serializer = WorkingHoursSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, working_hours_pk):
        query = get_object_or_404(WorkingHours.objects, institution_id=pk, pk=working_hours_pk)
        serializer = WorkingHoursSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, working_hours_pk):
        query = get_object_or_404(WorkingHours.objects, institution_id=pk, pk=working_hours_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)