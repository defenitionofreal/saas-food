from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.product.models import Product, Modifier
from apps.base.authentication import JWTAuthentication


class CreateOrDeleteModifiersClientAPIView(APIView):
    """
    Customer can add modifiers to a product
    - product total price rises
    - can add multiple additives
    - if modifier already exists than delete it
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain, product_slug, modifier_pk):
        institution = Institution.objects.get(domain=domain)
        product = Product.objects.get(institution=institution,
                                      slug=product_slug)
        modifier = get_object_or_404(Modifier.objects,
                                     id=modifier_pk,
                                     institution=institution)
        modifier_price = modifier.modifiers_price.select_related(
            'modifier').filter(product=product,
                               institution=institution)

        session = self.request.session
        product_with_options = session.get('product_with_options')

        if not product_with_options:
            product_with_options = session['product_with_options'] = {}
        product_with_options = product_with_options

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

        if not modifier_price:
            return Response({
                "detail": f"{product.title} doesn't have this modifier"},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            if not "modifiers" in product_dict[product.slug]:
                product_dict[product.slug]["modifiers"] = {}
            for mod in modifier_price:
                product_dict[product.slug]["modifiers"] = {
                    mod.modifier.id: {"title": mod.modifier.title,
                                      "price": int(mod.price)}}
                product_dict[product.slug]["price"] = int(mod.price)

        session.modified = True
        return Response({"product_with_options": product_with_options})
