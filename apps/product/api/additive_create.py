from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.product.serializers import AdditiveSerializer
from apps.company.models import Institution
from apps.product.models import CategoryAdditive


class AdditiveCreateAPIView(APIView):
    """ Create new additive """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AdditiveSerializer(data=request.data)
        institution = Institution.objects.filter(user=self.request.user)
        additievs_cats = CategoryAdditive.objects.filter(
            user=self.request.user)

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

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
