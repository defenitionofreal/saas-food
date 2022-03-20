from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.product.models import Product, Modifier
from apps.base.authentication import JWTAuthentication
from apps.showcase.services.product_session_class import ProductSessionClass


class CreateOrDeleteModifiersClientAPIView(APIView):
    """
    Customer can add modifier to a product
    - product price changes to a modifier price
    - can add only one modifier:
     - if modifier already exists than do nothing
     - if select new modifier than change old one to a new
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
        product_session = ProductSessionClass(session, "product_with_options")
        product_session.check_product_with_options_obj()
        product_session.check_product_obj(product)
        product_session.check_product_slug_obj(product)
        product_session.check_product_stickers(product)
        product_dict = product_session.product_dict()

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
        return Response({"product_with_options": product_session.check_product_with_options_obj()})
