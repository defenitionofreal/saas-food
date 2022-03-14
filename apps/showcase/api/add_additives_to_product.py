from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from apps.company.models import Institution
from apps.product.models import Product, Additive, CategoryAdditive
from apps.product.serializers import ProductSerializer, Additive, CategoryAdditive
from apps.base.authentication import JWTAuthentication


class AddAdditivesClientAPIView(APIView):
    """
    Customer can add additives to a product
    - products price rises
    - can add multiple additives
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, domain, product_slug, additive_pk):
        institution = Institution.objects.get(domain=domain)
        additive = get_object_or_404(Additive, slug=additive_pk)
        user = self.request.user

        return Response({"detail": "we working..."})
