from rest_framework.views import APIView
from apps.company.models import Institution
from apps.order.services.delivery_helper import DeliveryHelper


class DeliveryInfoAPIView(APIView):
    """
    Delivery info create/update by customer
    """

    def post(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        user = self.request.user
        session = self.request.session.session_key

        delivery_type = request.data['delivery_type']
        address = request.data['address']
        order_date = request.data.get("order_date", None)

        delivery_helper = DeliveryHelper(request,
                                         institution,
                                         delivery_type,
                                         address,
                                         user,
                                         session,
                                         order_date)

        return delivery_helper.set_delivery_info()
