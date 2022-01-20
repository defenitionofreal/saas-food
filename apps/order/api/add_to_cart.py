from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from apps.product.models import Product
from apps.company.models import Institution
from apps.order.models import OrderItem, Cart, CartItem
from apps.order.serializers import CartSerializer, CartItemSerializer

from apps.base.authentication import JWTAuthentication


class AddToCartAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, domain, product_id):
        user = self.request.user
        institution = Institution.objects.get(domain=domain)
        item = get_object_or_404(Product, id=product_id)

        # quantity = self.request.query_params.get('quantity')
        if user.is_authenticated and user.is_customer:
            # scopes problem
            # print(user)
            cart_qs = Cart.objects.get_or_create(institution=institution,
                                                 customer=self.request.user)
            return Response({"detail": "we working"})
        else:
            # make it that guest user can create cart
            # print(user)
            return Response({"detail": "Authorize to add product to an order."})

        # cart_item, created = CartItem.objects.get_or_create(
        #     cart=cart_qs,
        #     product=item,
        #     quantity=quantity
        # )

        if cart_qs:
            cart = cart_qs[0]
            print(cart)
        else:
            return Response({"detail": "cart"})
        #     if cart.items.filter(item__slug=item.slug).exists():
        #         cart_item.quantity += 1
        #         cart_item.save()
        #         return Response(
        #             {"detail": "This item quantity was updated."})
        #     else:
        #         cart.items.add(cart_item)
        #         return Response(
        #             {"detail": "This item was added to your cart."})
        # else:
        #     cart = Cart.objects.create(
        #         institution=institution)
        #     cart.items.add(cart_item)
        #     return Response(
        #         {"detail": "Cart created. This item was added to your cart."})
        # serializer.save(cart=cart_qs,
        #             product=item,
        #             quantity=quantity)



        # serializer = CartItemSerializer(data=request.data)
        # if serializer.is_valid():
        #
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     if item:
        #         if item == item.product.slug:
        #             serializer.save(product=item)
        #             return Response(serializer.data,
        #                             status=status.HTTP_201_CREATED)
        #         else:
        #             raise ValidationError({"error": "wrong product."})
        #     else:
        #         raise ValidationError({"error": "product was not provided."})
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
