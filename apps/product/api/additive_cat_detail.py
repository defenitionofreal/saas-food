from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.product.serializers import CategoryAdditiveSerializer
from apps.product.models import CategoryAdditive

from apps.company.models import Institution
from apps.company.services.compare_institution import _find_wrong_inst_id


class CategoryAdditiveDetailAPIView(APIView):
    """
    Retrieve, update or delete a additive category.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, additive_cat_pk):
        query = get_object_or_404(CategoryAdditive.objects,
                                  user=self.request.user,
                                  pk=additive_cat_pk)
        serializer = CategoryAdditiveSerializer(query)
        return Response(serializer.data)

    def put(self, request, additive_cat_pk):
        institution = Institution.objects.filter(user=self.request.user)
        if request.data["institution"]:
            if _find_wrong_inst_id(request.data["institution"],
                                   institution.values_list('id', flat=True)):
                return Response({"detail": f"wrong institution id"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "institution is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        query = get_object_or_404(CategoryAdditive.objects,
                                  user=self.request.user,
                                  pk=additive_cat_pk)
        serializer = CategoryAdditiveSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, additive_cat_pk):
        query = get_object_or_404(CategoryAdditive.objects,
                                  user=self.request.user,
                                  pk=additive_cat_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
