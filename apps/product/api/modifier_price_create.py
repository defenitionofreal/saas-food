from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.product.serializers import ModifierPriceSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import Institution
from apps.product.models import Modifier


class ModifierPriceCreateAPIView(APIView):
    """ Create new modifier price """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, modifier_pk):
        serializer = ModifierPriceSerializer(data=request.data)
        institution = Institution.objects.get(pk=pk)
        modifier = Modifier.objects.get(pk=modifier_pk)
        if serializer.is_valid():
            serializer.save(institution=institution,
                            modifier=modifier)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
