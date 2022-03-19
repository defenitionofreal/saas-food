from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.product.models import Product, Additive
from apps.base.authentication import JWTAuthentication


class CreateOrDeleteAdditivesClientAPIView(APIView):
    """
    Customer can add additives to a product
    - products total price rises
    - can add multiple additives
    - if additive adready exists than delete it
    """
    authentication_classes = [JWTAuthentication]
    # TODO: detail product/cart view with options if exists
    # TODO: add sticker dict to a product array

    def post(self, request, domain, product_slug, additive_pk):
        institution = Institution.objects.get(domain=domain)
        product = Product.objects.get(institution=institution,
                                      slug=product_slug)
        additive = get_object_or_404(Additive.objects,
                                     id=additive_pk,
                                     institution=institution,
                                     is_active=True)

        product_additive_cat = product.additives.select_related(
            'institution').filter(is_active=True)

        if not product_additive_cat:
            return Response({
                "detail": f"{product.title} doesn't have this additive"},
                status=status.HTTP_400_BAD_REQUEST)

        session = self.request.session
        product_with_options = session.get('product_with_options')
        if not product_with_options:
            product_with_options = session['product_with_options'] = {}
        product_with_options = product_with_options
        # del product_with_options
        # self.request.session.flush()
        if not "product" in product_with_options:
            product_with_options["product"] = {
                product.slug: {"title": product.title,
                               "price": int(product.price),
                               "total": int(product.price)}}

        if not str(product.slug) in product_with_options["product"].keys():
            product_with_options["product"].update({
                product.slug: {"title": product.title,
                               "price": int(product.price),
                               "total": int(product.price)}})

        a_id = str(additive.id)
        a_price = int(additive.price)
        product_dict = product_with_options["product"]

        if any(additive in cat.category_additive.filter(is_active=True)
               for cat in product_additive_cat):
            if "additives" in product_dict[product.slug]:
                if a_id in product_dict[product.slug]["additives"].keys():
                    product_dict[product.slug]["total"] -= a_price
                    del product_dict[product.slug]["additives"][a_id]
                else:
                    product_dict[product.slug]["additives"].update(
                        {additive.id: {"name": additive.title,
                                       "price": a_price,
                                       "counter": 1}})
                    product_dict[product.slug]["total"] += a_price
            else:
                product_dict[product.slug]["additives"] = {
                    additive.id: {"name": additive.title,
                                  "price": a_price,
                                  "counter": 1}}
                product_dict[product.slug]["total"] += a_price
            session.modified = True
            return Response(
                {"product_with_options": product_with_options})
        else:
            return Response(
                {"detail": f"{additive.title} tied to another category"},
                status=status.HTTP_400_BAD_REQUEST)
