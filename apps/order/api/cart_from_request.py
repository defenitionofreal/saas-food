from django.conf import settings
from apps.company.models import Institution
from apps.order.models import Cart


def get_cart_from_request(request, domain):
    institution = Institution.objects.get(domain=domain)
    user = request.user
    session = request.session

    if user.is_authenticated:
        return Cart.objects.get(institution=institution, customer=user)
    else:
        if settings.CART_SESSION_ID in session:
            return Cart.objects.get(institution=institution,
                                    session_id=session[settings.CART_SESSION_ID])

def get_or_create_cart_from_request(request, domain):
    institution = Institution.objects.get(domain=domain)
    user = request.user
    session = request.session

    if user.is_authenticated:
        return Cart.objects.get_or_create(institution=institution, customer=user,
                                          session_id=session[settings.CART_SESSION_ID])
    else:
        return Cart.objects.get_or_create(institution=institution, session_id=session[settings.CART_SESSION_ID])
