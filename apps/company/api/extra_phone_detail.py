from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.serializers import ExtraPhoneSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import ExtraPhone


class ExtraPhoneDetailAPIView(APIView):
    """
    Retrieve, update or delete a phones.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, extra_phones_pk):
        query = get_object_or_404(ExtraPhone.objects, institution_id=pk, pk=extra_phones_pk)
        serializer = ExtraPhoneSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, extra_phones_pk):
        query = get_object_or_404(ExtraPhone.objects, institution_id=pk, pk=extra_phones_pk)
        serializer = ExtraPhoneSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, extra_phones_pk):
        query = get_object_or_404(ExtraPhone.objects, institution_id=pk, pk=extra_phones_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
