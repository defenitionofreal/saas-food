from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status

from apps.base.serializers import UserSerializer
from apps.order.serializers import CartDashboardSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerViewSet(viewsets.ModelViewSet):
    """
    Customer view set is for all customer's dashboard information.
    (read/update: profile, delivery addresses, phone numbers, past orders,
     bonuses, order status, repeat order, live queue status...)
    """
    queryset = User.objects.filter(is_customer=True)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user if user.is_customer else None

    def get_serializer_class(self):
        pass

    @action(detail=False, methods=['get'], url_path='orders')
    def orders(self, request):
        """
        List all statuses orders by user but can use filter to a needed status.
        """
        user = self.get_queryset()
        if not user:
            return

        order_status = self.request.query_params.get("status", None)
        orders = user.cart_customer.all()
        if order_status:
            orders = user.cart_customer.filter(status=order_status)

        serializer = CartDashboardSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
