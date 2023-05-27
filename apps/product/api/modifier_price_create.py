from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.product.serializers import ModifierPriceSerializer
from apps.company.models import Institution
from apps.product.models import Modifier, Product

# TODO: нужно ли логику филиала убрать?
class ModifierPriceCreateAPIView(APIView):
    """ Create new modifier price """
    permission_classes = [IsAuthenticated]

    def post(self, request, modifier_pk):
        serializer = ModifierPriceSerializer(data=request.data)
        modifier = Modifier.objects.get(pk=modifier_pk)
        product = Product.objects.filter(user=self.request.user)
        # institution = Institution.objects.filter(user=self.request.user)
        #
        # if request.data["institution"]:
        #     if _find_wrong_inst_id(request.data["institution"],
        #                            institution.values_list('id', flat=True)):
        #         return Response({"detail": f"wrong institution id"},
        #                         status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"detail": "institution is required"},
        #                     status=status.HTTP_400_BAD_REQUEST)

        if not request.data["product"] or request.data["product"] is None:
            return Response({"detail": "product is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data["product"] not in product.values_list('id',
                                                               flat=True):
            return Response({"detail": "wrong product id"},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(user=self.request.user,
                            modifier=modifier)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
