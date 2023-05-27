from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.product.models import Modifier
from apps.product.serializers import ModifierSerializer

from apps.company.models import Institution


class ModifierDetailAPIView(APIView):
    """
    Retrieve, update or delete a modifier.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, modifier_pk):
        query = get_object_or_404(Modifier.objects,
                                  user=self.request.user,
                                  pk=modifier_pk)
        serializer = ModifierSerializer(query)
        return Response(serializer.data)

    def put(self, request, modifier_pk):
        # institution = Institution.objects.filter(user=self.request.user)
        # if request.data["institution"]:
        #     if _find_wrong_inst_id(request.data["institution"],
        #                            institution.values_list('id', flat=True)):
        #         return Response({"detail": f"wrong institution id"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"detail": "institution is required"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        query = get_object_or_404(Modifier.objects,
                                  user=self.request.user,
                                  pk=modifier_pk)
        serializer = ModifierSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, modifier_pk):
        query = get_object_or_404(Modifier.objects,
                                  user=self.request.user,
                                  pk=modifier_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
