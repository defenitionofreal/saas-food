from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.payment.models import PaymentTypeInstitution
from apps.payment.serializers import PaymentTypeInstitutionSerializer

from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission
)


class PaymentTypeInstitutionViewSet(viewsets.ModelViewSet):

    queryset = PaymentTypeInstitution.objects.all()
    serializer_class = PaymentTypeInstitutionSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
