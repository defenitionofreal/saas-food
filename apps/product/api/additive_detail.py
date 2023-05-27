from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.product.serializers import AdditiveSerializer
from apps.product.models import Additive, CategoryAdditive

from apps.company.models import Institution


class AdditiveDetailAPIView(APIView):
    """
    Retrieve, update or delete a additive.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, additive_pk):
        query = get_object_or_404(Additive.objects,
                                  user=self.request.user,
                                  pk=additive_pk)
        serializer = AdditiveSerializer(query)
        return Response(serializer.data)

    def put(self, request, additive_pk):
        additievs_cats = CategoryAdditive.objects.filter(
            user=self.request.user)

        # institution = Institution.objects.filter(user=self.request.user)
        # if request.data["institution"]:
        #     if _find_wrong_inst_id(request.data["institution"],
        #                            institution.values_list('id', flat=True)):
        #         return Response({"detail": f"wrong institution id"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"detail": "institution is required"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        if not request.data["category"] or request.data["category"] is None:
            return Response({"detail": "category is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data["category"] not in additievs_cats.values_list('id',
                                                                      flat=True):
            return Response({"detail": "wrong category id"},
                            status=status.HTTP_400_BAD_REQUEST)

        query = get_object_or_404(Additive.objects,
                                  user=self.request.user,
                                  pk=additive_pk)
        serializer = AdditiveSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, additive_pk):
        query = get_object_or_404(Additive.objects,
                                  user=self.request.user,
                                  pk=additive_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
