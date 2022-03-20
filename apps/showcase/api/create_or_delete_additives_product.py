from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.product.models import Product, Additive
from apps.base.authentication import JWTAuthentication
from apps.showcase.services.product_session_class import ProductSessionClass


class CreateOrDeleteAdditivesClientAPIView(APIView):
    """
    Customer can add additives to a product
    - products additives_price rises
    - can add multiple additives
    - if additive already exists than delete it
      if not than update an additives array with it
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

        product_additive_cat = product.additives.select_related(
            'institution').filter(is_active=True)

        if not product_additive_cat:
            return Response({
                "detail": f"{product.title} doesn't have this additive"},
                status=status.HTTP_400_BAD_REQUEST)

        session = self.request.session
        product_session = ProductSessionClass(session, "product_with_options")
        # product_session.del_product_in_session()
        # product_session.del_session()
        product_session.check_product_with_options_obj()
        product_session.check_product_obj(product)
        product_session.check_product_slug_obj(product)
        product_session.check_product_stickers(product)
        product_dict = product_session.product_dict()

        a_id = str(additive.id)
        a_price = int(additive.price)
        if any(additive in cat.category_additive.filter(is_active=True)
               for cat in product_additive_cat):
            if "additives" in product_dict[product.slug]:
                if a_id in product_dict[product.slug]["additives"].keys():
                    product_dict[product.slug]["additives_price"] -= a_price
                    del product_dict[product.slug]["additives"][a_id]
                else:
                    product_dict[product.slug]["additives"].update(
                        {additive.id: {"title": additive.title,
                                       "price": a_price,
                                       "counter": 1}})
                    product_dict[product.slug]["additives_price"] += a_price
            else:
                product_dict[product.slug]["additives"] = {
                    additive.id: {"title": additive.title,
                                  "price": a_price,
                                  "counter": 1}}
                product_dict[product.slug]["additives_price"] += a_price
            session.modified = True
            return Response(
                {"product_with_options": product_session.check_product_with_options_obj()})
        else:
            return Response(
                {"detail": f"{additive.title} tied to another category"},
                status=status.HTTP_400_BAD_REQUEST)
