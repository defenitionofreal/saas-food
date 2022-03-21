from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.company.models import Institution
from apps.product.models import Product, ModifierPrice
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
        modifier_qs = get_object_or_404(ModifierPrice.objects,
                                        id=modifier_pk,
                                        product=product,
                                        institution=institution)

        session = self.request.session
        product_session = ProductSessionClass(session, "product_with_options")
        product_session.main(product)
        product_dict = product_session.product_dict()

        if not "modifiers" in product_dict[product.slug]:
            product_dict[product.slug]["modifiers"] = {}

        product_dict[product.slug]["modifiers"] = {
            modifier_qs.id: {"title": modifier_qs.modifier.title,
                             "price": int(modifier_qs.price)}}
        product_dict[product.slug]["price"] = int(modifier_qs.price)

        session.modified = True
        response = product_session.check_product_with_options_obj()
        return Response({"product_with_options": response})
