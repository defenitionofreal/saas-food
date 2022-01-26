from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.company.serializers import MinCartCostSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import Institution, MinCartCost


class MinCartCostCreateAPIView(APIView):
    """ Create new or update old rule for a minimal cart cost """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            serializer = MinCartCostSerializer(data=request.data)
            institution = Institution.objects.get(pk=pk)

            if serializer.is_valid():
                cart_cost, created = MinCartCost.objects.update_or_create(
                    institution=institution,
                    defaults={
                        "cost": serializer.validated_data['cost']
                    })

                cart_cost.cost = serializer.validated_data['cost']
                cart_cost.save()

                if created:
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{e}"})
