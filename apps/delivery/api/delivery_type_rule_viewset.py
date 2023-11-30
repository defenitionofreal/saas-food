from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from apps.delivery.models import DeliveryTypeRule
from apps.delivery.serializers import DeliveryTypeRuleSerializer

from apps.authentication.permissions import (
    ConfirmedAccountPermission, OrganizationPermission
)


class DeliveryTypeRuleViewSet(viewsets.ModelViewSet):

    queryset = DeliveryTypeRule.objects.all()
    serializer_class = DeliveryTypeRuleSerializer
    permission_classes = [IsAuthenticated,
                          ConfirmedAccountPermission,
                          OrganizationPermission]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    # @action(detail=False,
    #         methods=["get"],
    #         permission_classes=[AllowAny],
    #         url_path="delivery-types")
    # def delivery_types(self, request):
    #     """
    #
    #     """
    #     institution_id = request.data['institution_id']
    #     institution = Institution.objects.filter(id=institution_id).first()
    #     if not institution:
    #         raise ValidationError({"detail": "Wrong institution"})

