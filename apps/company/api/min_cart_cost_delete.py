from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.company.models import MinCartCost
from apps.base.authentication import JWTAuthentication


class MinCartCostDeleteAPIView(APIView):
    """
    delete MinCartCost.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, rule_pk):
        query = get_object_or_404(MinCartCost.objects, institution_id=pk,
                                  pk=rule_pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
