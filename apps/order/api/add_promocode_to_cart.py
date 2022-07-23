from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from apps.company.models import Institution
from apps.order.models import PromoCode
from apps.order.services.cart_helper import CartHelper


class AddPromoCodeAPIView(APIView):
    """ Add coupon to cart """

    def post(self, request, domain, coupon):
        promo_code = get_object_or_404(PromoCode, code=coupon)
        institution = Institution.objects.get(domain=domain)
        cart_helper = CartHelper(request=request, institution=institution)
        return cart_helper.add_promo_code(promo_code)
