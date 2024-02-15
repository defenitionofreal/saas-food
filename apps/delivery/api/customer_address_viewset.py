from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings

from apps.company.models import Institution
from apps.delivery.models import CustomerAddress, CartDeliveryInfo
from apps.delivery.models.enums import DeliveryType
from apps.delivery.serializers import (
    CustomerAddressSerializer, CartDeliveryInfoSerializer
)
from apps.delivery.services.geocoder import KladrSuggestions

from apps.authentication.permissions import (
    ConfirmedAccountPermission, CustomerPermission
)
from apps.delivery.services.utils import (
    merge_customer_address, delete_customer_last_duplicated_addresses,
    get_delivery_type_rule, has_zones_and_delivery_zone_object
)
from apps.order.services.cart_helper import CartHelper


class CustomerAddressViewSet(viewsets.ModelViewSet):
    """
    View for a customer (guest/auth) user to crud self delivery address
    and also actions to get affiliate delivery points, zones and set
    cart delivery information.
    """
    queryset = CustomerAddress.objects.all()
    serializer_class = CustomerAddressSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        """ auth on destroy, update methods """
        if self.action in ("destroy", "update"):
            return (IsAuthenticated(),)
        return super(CustomerAddressViewSet, self).get_permissions()

    def get_queryset(self):
        """ get address by session or by auth user """
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        session_id = self.request.session.session_key if self.request.session else None
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset.filter(session_id=session_id)

    def create(self, request, *args, **kwargs):
        """
        create customer address after geocoder !but GET address data
        if it already exists under the same session or user.
        """
        user_id = self.request.user.id if (self.request.user.is_authenticated and self.request.user.is_customer) else None
        session_id = self.request.session.session_key if self.request.session else None

        institution_id = request.data.get("institution_id", None)
        query = request.data.get("query", None)
        additional_address_info = request.data.get("additional_address_info", None)

        institution = Institution.objects.get(id=institution_id)
        geocoder_token = institution.user.yandexgeocodertoken_set.first()

        kladr = KladrSuggestions(settings.KLADR_API_KEY)
        address_detail = kladr.address_detail(geocoder_token.api_key, query)
        valid_address = kladr.address_data_after_yandex_geocoder(address_detail)
        if additional_address_info:
            valid_address.update(additional_address_info)

        # get or create to validate duplicates
        if user_id:
            valid_address.update({"session_id": session_id})
            address, _ = CustomerAddress.objects.get_or_create(
                user_id=user_id,
                display_name=valid_address["display_name"],
                defaults=valid_address
            )
        else:
            valid_address.update({"user": user_id})
            address, _ = CustomerAddress.objects.get_or_create(
                session_id=session_id,
                display_name=valid_address["display_name"],
                defaults=valid_address
            )

        serializer = CustomerAddressSerializer(address)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.request.user.is_authenticated:
            session_id = self.request.session.session_key
            user_id = self.request.user.id
            merge_customer_address(session_id, user_id)
            delete_customer_last_duplicated_addresses(user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # todo: make retrieve auth?
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="set-cart-delivery-info")
    def set_cart_delivery_info(self, request):
        """
        Set pickup or courier type, so that address will be at response.
        Also validates delivery zone logic if courier type.
        params: institution_id, delivery_type, customer_address_id
        """
        # todo: delivery date and time ???
        institution_address = None
        customer_address = None
        delivery_zone = None

        institution_id = request.data['institution_id']
        institution = Institution.objects.filter(id=institution_id).first()
        if not institution:
            raise ValidationError({"detail": "Wrong institution"})

        delivery_type_str = request.data['delivery_type']
        delivery_type_rule = get_delivery_type_rule(delivery_type_str, institution_id)
        if not delivery_type_rule:
            raise ValidationError({"detail": "Wrong delivery type"})

        if delivery_type_rule.delivery_type in (DeliveryType.PICKUP, DeliveryType.INDOOR):
            institution_address = institution.institutionaddress_set.first()

        if delivery_type_rule.delivery_type == DeliveryType.COURIER:
            customer_address_id = request.data.get("customer_address_id", None)
            if not customer_address_id:
                raise ValidationError({"detail": "Wrong customer address"})

            custom_filter = {"id": customer_address_id}
            if self.request.user.is_authenticated:
                custom_filter["user_id"] = self.request.user.id
            else:
                custom_filter["session_id"] = self.request.session.session_key

            try:
                customer_address = CustomerAddress.objects.get(**custom_filter)
            except CustomerAddress.DoesNotExist:
                raise ValidationError({"detail": "Address not found."})

            has_active_zones, delivery_zone = has_zones_and_delivery_zone_object(
                institution,
                customer_address.latitude,
                customer_address.longitude
            )
            if has_active_zones and not delivery_zone:
                raise ValidationError({"detail": "Address not included at delivery zones"})

        cart, _ = CartHelper(request, institution).cart_get_or_create()
        cart_delivery_info, _ = CartDeliveryInfo.objects.update_or_create(
            cart_id=cart.id,
            defaults={
                "type": delivery_type_rule,
                "zone": delivery_zone,
                "customer_address": customer_address,
                "institution_address": institution_address
            }
        )
        serializer = CartDeliveryInfoSerializer(cart_delivery_info)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def delivery_zones(self, request):
        # todo:
        pass

    @action(detail=False, methods=["get"])
    def delivery_points(self, request):
        # todo:
        pass
