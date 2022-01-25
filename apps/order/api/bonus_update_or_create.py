from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.order.serializers import BonusSerializer
from apps.base.authentication import JWTAuthentication
from apps.company.models import Institution
from apps.order.models import Bonus


class BonusCreateAPIView(APIView):
    """ Create new or update old rule for a bonus """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            serializer = BonusSerializer(data=request.data)
            institution = Institution.objects.get(pk=pk)

            if serializer.is_valid():
                if serializer.is_valid():
                    serializer.save(institution=institution)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                # bonus, created = Bonus.objects.update_or_create(
                #     institution=institution)
                #
                # bonus.is_active = serializer.validated_data['is_active']
                # bonus.write_off = serializer.validated_data['write_off']
                # bonus.accrual = serializer.validated_data['accrual']
                # bonus.is_promo_code = serializer.validated_data[
                #     'is_promo_code']
                # bonus.is_registration_bonus = serializer.validated_data[
                #     'is_registration_bonus']
                # bonus.registration_bonus = serializer.validated_data[
                #     'registration_bonus']
                # bonus.save()
                # #serializer.save(institution=institution)
                # if created:
                #     return Response(serializer.data,
                #                     status=status.HTTP_201_CREATED)
                # else:
                #     return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{e}"})
