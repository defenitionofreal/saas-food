from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from apps.company.models import Institution
from apps.order.models import PromoCode
from apps.order.services.cart_helper import CartHelper


class AddPromoCodeAPIView(APIView):
    """ Add coupon to cart """

    def post(self, request, domain, coupon):
        code = get_object_or_404(PromoCode, code=coupon)
        institution = Institution.objects.get(domain=domain)
        cart = CartHelper(request, institution)
        return cart.add_coupon(code)


