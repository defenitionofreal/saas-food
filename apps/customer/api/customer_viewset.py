from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status

from apps.base.serializers import UserSerializer
from apps.que.serializers import QueSerializer
from apps.location.serializers import AddressSerializer

from apps.location.models import (Address, AddressLink)
from apps.que.models.enums.que_status import QueStatus
from apps.que.models import Que
from apps.order.serializers import (
    CartDashboardSerializer, CartSerializer, UserBonusSerializer
)

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerViewSet(viewsets.ModelViewSet):
    """
    Customer view set is for all customer's dashboard information.
    (read/update: profile, delivery addresses, phone numbers, past orders,
     bonuses, order status, repeat order, live queue status...)
    """
    queryset = User.objects.filter(is_customer=True, is_organization=False)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user if user.is_customer else None

    def get_serializer_class(self):
        pass

    @action(detail=False, methods=["get", "put"], url_path="profile")
    def profile(self, request):
        """
        Detail profile view
        """
        user = self.get_queryset()

        if request.method == "PUT":
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, many=False, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get", "post"], url_path="address")
    def address(self, request):
        """ Address List and Create view"""
        if request.method == "POST":
            serializer = AddressSerializer(data=request.data)
            if serializer.is_valid():
                address = serializer.save()
                AddressLink.objects.create(
                    user_id=self.request.user.id,
                    address_id=address.id
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        user = self.get_queryset()
        user_address_links = user.addresslink_set.all() if user else None
        if not user_address_links:
            return Response({"detail": "Addresses not found"},
                            status=status.HTTP_404_NOT_FOUND)

        user_addreses = Address.objects.filter(id__in=[link.address.id for link in user_address_links])
        serializer = AddressSerializer(user_addreses, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["get", "put", "delete"],
            url_path="address/(?P<address_id>[^/.]+)")
    def address_detail(self, request, address_id=None):
        """ Address detail R.U.D. view """
        user_address = Address.objects.get(id=address_id)
        serializer = AddressSerializer(
            user_address, many=False, read_only=True
        )
        if request.method == "PUT":
            serializer = AddressSerializer(user_address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        if request.method == "DELETE":
            user_address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data)

    @action(detail=False, methods=["get", "put"], url_path="phone")
    def phone(self, request):
        # todo: нужна таблица для того чтобы иметь несколько номеров
        pass

    @action(detail=False, methods=["get"], url_path="queue")
    def queue(self, request):
        """
        Live queue view to check queue status (Cooking/Ready) of an order at
        affiliate.
        """
        user = self.get_queryset()
        user_order_ids = user.cart_customer.values_list("id", flat=True) if user else None
        user_queue = Que.objects.filter(
            order_id__in=user_order_ids,
            status__in=[QueStatus.COOKING, QueStatus.READY],
            is_active=True
        )
        if not user_queue.exists():
            return Response({"detail": "Queue not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = QueSerializer(user_queue, many=True, read_only=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="bonuses")
    def bonuses(self, request):
        user = self.get_queryset()
        user_bonuses = user.userbonus_set.all() if user else None
        if not user_bonuses:
            return Response({"detail": "Bonuses not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserBonusSerializer(user_bonuses, many=True,
                                         read_only=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="orders")
    def orders(self, request):
        """
        List all statuses orders by user but can use filter to a needed status.
        """
        user = self.get_queryset()
        order_status = self.request.query_params.get("status", None)
        orders = user.cart_customer.all() if user else None
        if not orders:
            return Response({"detail": "Orders not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if order_status:
            orders = user.cart_customer.filter(status=order_status)

        serializer = CartDashboardSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"],
            url_path="orders/(?P<order_id>[^/.]+)")
    def orders_detail(self, request, order_id=None):
        """
        Order detail view
        """
        user = self.get_queryset()
        order = user.cart_customer.filter(id=order_id).first() if user else None
        if not order:
            return Response({"detail": "Order not found"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(order, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"],
            url_path="orders/(?P<order_id>[^/.]+)/repeat")
    def order_repeat(self, request, order_id=None):
        pass

    @action(detail=False, methods=["get"],
            url_path="orders/(?P<order_id>[^/.]+)/cancel")
    def order_cancel(self, request, order_id=None):
        pass
