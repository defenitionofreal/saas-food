from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import Http404

from apps.company.serializers import DesignSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import Design, Institution


class DesignDetailAPIView(APIView):
    """
    Retrieve, update or delete a design instance.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Design.objects.get(pk=pk)
        except Institution.DoesNotExist:
            raise Http404

    def get(self, request, pk, id):
        #institution = self.get_object(pk)
        institution = Institution.objects.get(pk=pk)
        design = Design.objects.filter(institution=institution)
        serializer = DesignSerializer(design)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     institution = self.get_object(pk)
    #     serializer = DesignSerializer(institution, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     institution = self.get_object(pk)
    #     institution.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)