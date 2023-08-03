from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.company.models import Institution
from apps.order.serializers import CartSerializer
from apps.order.models import Cart, PromoCode, PromoCodeUser

from apps.order.models.enums.order_status import OrderStatus
from apps.order.services.cart_helper import CartHelper


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.filter(status=OrderStatus.DRAFT)
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        domain = self.kwargs.get('domain')
        institution = Institution.objects.get(domain=domain)
        queryset = Cart.objects.filter(
            customer=self.request.user,
            institution=institution
        ).order_by("-id")
        return queryset

    def list(self, request, *args, **kwargs):
        domain = self.kwargs.get('domain')
        institution = Institution.objects.get(domain=domain)
        helper = CartHelper(request, institution)

        cart = helper.get_cart()
        if not cart:
            raise ValidationError({"detail": "No cart."})

        serializer = self.get_serializer(cart, many=False,
                                         context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET", detail="Method not allowed.")

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST", detail="Method not allowed.")

    @action(detail=False, methods=["post"])
    def add(self, request, *args, **kwargs):
        domain = self.kwargs.get('domain')
        institution = Institution.objects.get(domain=domain)
        helper = CartHelper(request, institution)
        helper.add_item()
        cart = helper.get_cart()
        serializer = self.get_serializer(
            cart, many=False, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def remove(self, request, *args, **kwargs):
        domain = self.kwargs.get('domain')
        institution = Institution.objects.get(domain=domain)
        item_hash = request.data.get("item_hash", None)
        helper = CartHelper(request, institution)
        helper.remove_item(item_hash)
        cart = helper.get_cart()
        serializer = self.get_serializer(
            cart, many=False, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add-coupon")
    def add_coupon(self, request, *args, **kwargs):
        domain = self.kwargs.get('domain')
        institution = Institution.objects.get(domain=domain)
        code = self.request.data.get("code", None)
        code = get_object_or_404(PromoCode, code=code, institutions=institution)
        helper = CartHelper(request, institution)
        helper.add_coupon(code)
        cart = helper.get_cart()
        serializer = self.get_serializer(
            cart, many=False, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="remove-coupon")
    def remove_coupon(self, request, *args, **kwargs):
        domain = self.kwargs.get('domain')
        institution = Institution.objects.get(domain=domain)
        helper = CartHelper(request, institution)
        cart = helper.get_cart()
        coupon = cart.promo_code
        if coupon:
            user_coupon = PromoCodeUser.objects.get(
                code_id=coupon.id, user_id=cart.customer.id
            )
            user_coupon.num_uses -= 1
            user_coupon.save()
            coupon.num_uses -= 1
            coupon.save()
            cart.promo_code = None
            cart.save()

        serializer = self.get_serializer(
            cart, many=False, context={"request": request}
        )
        return Response(serializer.data)
