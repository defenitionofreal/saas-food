from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.product.models import Product, Additive, CategoryAdditive
from apps.product.serializers import ProductSerializer, AdditiveSerializer, \
    CategorySerializer
from apps.base.authentication import JWTAuthentication

from decimal import Decimal


def product_price_with_additive_func(categories, additive, product):
    for additive_cat in categories:
        if additive in additive_cat.category_additive.filter(
                is_active=True):
            product_price_with_additive = product.price
            product_price_with_additive += additive.price
    return product_price_with_additive


class CreateOrDeleteAdditivesClientAPIView(APIView):
    """
    Customer can add additives to a product
    - products total price rises
    - can add multiple additives
    - if additive adready exists than delete it
    """
    authentication_classes = [JWTAuthentication]
    # TODO: detail product/cart view with options if exists
    def post(self, request, domain, product_slug, additive_pk):
        institution = Institution.objects.get(domain=domain)
        product = Product.objects.get(institution=institution,
                                      slug=product_slug)
        additive = get_object_or_404(Additive.objects,
                                     id=additive_pk,
                                     institution=institution,
                                     is_active=True)

        session = self.request.session
        product_with_options = session.get('product_with_options')
        if not product_with_options:
            product_with_options = session['product_with_options'] = {}
        product_with_options = product_with_options

        # del product_with_options
        # self.request.session.flush()

        for additive_cat in product.additives.select_related(
                'institution').filter(is_active=True):
            if additive in additive_cat.category_additive.filter(
                    is_active=True):

                if not "product" in product_with_options:
                    product_with_options["product"] = {product.slug: {
                                                       "title": product.title,
                                                       "price": int(product.price),
                                                       "total": int(product.price)}}

                if not str(product.slug) in product_with_options["product"].keys():
                    product_with_options["product"].update({product.slug: {
                                                       "title": product.title,
                                                       "price": int(product.price),
                                                       "total": int(product.price)}})
                    print('yoo')

                if "additives" in product_with_options["product"][product.slug]:
                    if str(additive.id) in product_with_options["product"][product.slug]["additives"].keys():
                        product_with_options["product"][product.slug]["total"] -= product_with_options["product"][product.slug]["additives"][str(additive.id)]["price"]
                        del product_with_options["product"][product.slug]["additives"][str(additive.id)]
                    else:
                        product_with_options["product"][product.slug]["additives"].update(
                            {additive.id: {
                                     "name": additive.title,
                                     "price": int(additive.price),
                                     "counter": 1}})
                        product_with_options["product"][product.slug]["total"] += product_with_options["product"][product.slug]["additives"][additive.id]["price"]
                else:
                    product_with_options["product"][product.slug]["additives"] = {additive.id: {
                                     "name": additive.title,
                                     "price": int(additive.price),
                                     "counter": 1}}
                    product_with_options["product"][product.slug]["total"] += int(additive.price)

                session.modified = True
                return Response(
                    {"product_with_options": product_with_options})


        try:
            pass
            return Response(
                {"detail": f"{additive.title} from another category"},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"{e}"},
                            status=status.HTTP_400_BAD_REQUEST)
