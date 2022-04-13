from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.serializers import AnalyticsSerializer
from apps.company.models import Analytics


class AnalyticsDetailAPIView(APIView):
    """
    Retrieve, update or delete a design analytics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, analytics_pk):
        analytics = get_object_or_404(Analytics.objects, institution_id=pk, pk=analytics_pk)
        serializer = AnalyticsSerializer(analytics)
        return Response(serializer.data)

    def put(self, request, pk, analytics_pk):
        analytics = get_object_or_404(Analytics.objects, institution_id=pk, pk=analytics_pk)
        serializer = AnalyticsSerializer(analytics, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, analytics_pk):
        analytics = get_object_or_404(Analytics.objects, institution_id=pk, pk=analytics_pk)
        analytics.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
