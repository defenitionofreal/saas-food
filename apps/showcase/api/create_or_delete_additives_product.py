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
    - if additive already exists than delete it
      if not than update an array with it
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
                               "additives_price": 0}}

        if not str(product.slug) in product_with_options["product"].keys():
            product_with_options["product"].update({
                product.slug: {"title": product.title,
                               "price": int(product.price),
                               "additives_price": 0}})

        a_id = str(additive.id)
        a_price = int(additive.price)
        product_dict = product_with_options["product"]

        product_sticker = [i for i in product.sticker.filter(
                           is_active=True).order_by("id")]
        if product_sticker:
            product_dict[product.slug]["stickers"] = {
                sticker.id: {"title": sticker.title,
                             "bg_color": sticker.color,
                             "text_color": sticker.text_color}
                for sticker in product_sticker}
        else:
            product_dict[product.slug]["stickers"] = {}

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
                {"product_with_options": product_with_options})
        else:
            return Response(
                {"detail": f"{additive.title} tied to another category"},
                status=status.HTTP_400_BAD_REQUEST)
