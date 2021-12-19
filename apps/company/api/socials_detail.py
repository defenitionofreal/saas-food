from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.serializers import SocialLinksSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import SocialLinks


class SocialsDetailAPIView(APIView):
    """
    Retrieve, update or delete a design socials.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, socials_pk):
        query = get_object_or_404(SocialLinks.objects, institution_id=pk, pk=socials_pk)
        serializer = SocialLinksSerializer(query)
        return Response(serializer.data)

    def put(self, request, pk, socials_pk):
        query = get_object_or_404(SocialLinks.objects, institution_id=pk, pk=socials_pk)
        serializer = SocialLinksSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, socials_pk):
        query = get_object_or_404(SocialLinks.objects, institution_id=pk, pk=socials_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)