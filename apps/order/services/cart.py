from rest_framework.request import Request
from apps.order.models import Cart, CartProduct
from apps.product.models import Modifier, Additive, Product
from apps.company.models import Institution, MinCartCost
from django.conf import settings
from django.db import models
from apps.order.services.generate_cart_key import _generate_cart_key
import typing


class CartServiceException(Exception):
    """Cart service exception."""


class CartService:
    """Service for works with cart."""

    def get_cart(self, request: Request, domain: str) -> Cart:
        """Get user or anonymous cart."""
        institution = Institution.objects.get(domain=domain)
        user = request.user if (request.user and request.user.is_authenticated) else None

        session_cart_id = request.session.get(settings.CART_SESSION_ID)
        session_cart = Cart.objects.filter(
            institution=institution,
            session_id=session_cart_id,
        ).first()

        if user:
            user_cart = Cart.objects.filter(
                institution=institution,
                customer=user
            ).first()
            if user_cart:
                return user_cart

        if not session_cart:
            cart_cost = MinCartCost.objects.filter(institution=institution).first()
            min_amount = cart_cost.cost if cart_cost else None
            return Cart.objects.create(
                institution=institution,
                session_id=_generate_cart_key(),
                customer=user,
                min_amount=min_amount,
            )

        if session_cart and user:
            session_cart.customer = user
            session_cart.save()

        return session_cart

    def add_product(self, cart: Cart, product_data: typing.Dict[str, typing.Any]) -> None:
        """Validate and add product data to current cart."""
        validated_product_data = self._validate_product_data(cart, product_data)

        cart_product = CartProduct.objects.create(
            cart=cart,
            product=validated_product_data["product"],
            quantity=validated_product_data["quantity"],
        )

        cart_product.modifiers.set(validated_product_data["modifiers"])
        cart_product.additives.set(validated_product_data["additives"])

        # TODO: merge products

        return cart

    def calculate_cart_coast(self, cart: Cart) -> None:
        for cart_product in cart.cart_products.all():
            self._calculate_cart_product_coast(cart_product)

        # apply bonus
        # promo
        # delivery

        cart.total_coast = cart.cart_products.aggregate(total=models.Sum("total_coast"))["total"]

        cart.save()

    def _calculate_cart_product_coast(self, cart_product: CartProduct) -> None:
        sum_additives = cart_product.additives.aggregate(total=models.Sum("price"))["total"] or 0
        sum_modifiers = 0

        # TODO: implement subquery for getting modifier price
        for modifier in cart_product.modifiers.all():
            sum_modifiers += modifier.modifiers_price.first().price

        cart_product.price = cart_product.product.price + sum_additives + sum_modifiers

        # TODO: apply discount if exists it
        cart_product.discount = 0

        cart_product.total_coast = cart_product.quantity * cart_product.price - cart_product.discount
        cart_product.save()

    def _validate_product_data(self, cart: Cart, product_data: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
        if any((
                product_data["product"].institution != cart.institution,
                not product_data["product"].is_active,
                not product_data["product"].category.is_active,
        )):
            self._raise_not_found(Product)

        if product_data["quantity"] < 1:
            raise CartServiceException("Product quantity must be more 0.")

        for modifier in product_data["modifiers"]:
            if modifier.institution != cart.institution:
                self._raise_not_found(Modifier)

        for additive in product_data["additives"]:
            if additive.institution != cart.institution:
                self._raise_not_found(Additive)

        return product_data

    def _raise_not_found(self, model: models.Model) -> typing.NoReturn:
        raise model.DoesNotExist(
            "{0} matching query does not exist.".format(model.__class__._meta.object_name),
        )

"""
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        session = self.request.session
        cart_cost = MinCartCost.objects.filter(institution=institution).first()

        if user.is_authenticated:
            if settings.CART_SESSION_ID in session:
                session_cart = Cart.objects.filter(
                    institution=institution,
                    session_id=session[settings.CART_SESSION_ID]).first()
                if session_cart:
                    cart, cart_created = Cart.objects.get_or_create(
                        institution=institution, customer=user)

                    for item in session_cart.items.all():
                        item.cart = cart
                        item.save()

                        # TODO: count and add products not correctly. fix it!
                        product_filter = cart.items.filter(product__slug=item.product.slug)
                        if product_filter.exists():
                            for v in product_filter:
                                v.quantity += 1
                                v.save()
                            # item.quantity += 1
                            # item.save()
                        else:
                            cart.items.add(item)
                            cart.save()

                    if session_cart.promo_code:
                        cart.promo_code = session_cart.promo_code
                        cart.save()
                    session_cart.delete()
                    del session[settings.CART_SESSION_ID]
                    #session.flush()
                else:
                    # if no session cart
                    cart, cart_created = Cart.objects.get_or_create(
                        institution=institution, customer=user)
            else:
                cart = Cart.objects.filter(institution=institution,
                                           customer=user).first()
                if not cart:
                    return Response({"detail": "Cart does not exist. (auth cart)"})
        else:
            if not settings.CART_SESSION_ID in session:
                return Response({"detail": "Cart does not exist. (session cart)"})

            cart = Cart.objects.get(institution=institution,
                                    session_id=session[settings.CART_SESSION_ID])

        try:
            if cart_cost:
                cart.min_amount = cart_cost.cost
                cart.save()

            if cart.items.exists():
                serializer = CartSerializer(cart, context={"request": request})
                return Response(serializer.data)
            else:
                return Response({"detail": "Cart is empty."})
        except Exception as e:
            return Response({"detail": f"{e}"})

"""