from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.payment.serializers import YooMoneySerializer
from apps.payment.models import YooMoney


class YooMoneyCreateAPIView(APIView):
    """ Create new yoo money instance """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = YooMoneySerializer(data=request.data)
        if serializer.is_valid():
            yoo, created = YooMoney.objects.update_or_create(
                user=self.request.user,
                defaults={
                    "wallet": serializer.validated_data['wallet']
                })

            yoo.wallet = serializer.validated_data['wallet']
            yoo.save()

            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
