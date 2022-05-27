from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from apps.company.models import Institution
from apps.delivery.models import Delivery, DeliveryInfo
from apps.location.models import Address
from apps.delivery.serializers import DeliveryInfoSerializer
from apps.order.services.generate_cart_key import _generate_cart_key

from django.conf import settings



class DeliveryInfoAPIView(APIView):
    """
    Delivery info creat by customer
    """
    # делать модуль в корзине и привязывать к корзине по id и потом перекидывать днные в заказ
    # или привязывать к юзеру? Ну тогда нужна антентификация или же опять через сессии проробатывать
    # к юзеру логичней было бы! нужно додумать
    # к филиалу нет причин привязывать
    def post(self, request, domain, delivery_type_pk):
        institution = Institution.objects.get(domain=domain)
        delivery_type = get_object_or_404(Delivery, pk=delivery_type_pk)
        user = self.request.user

        # здесь я беру cart_id или создаю cart_id в сессии
        session = self.request.session
        if not settings.CART_SESSION_ID in session:
            session[settings.CART_SESSION_ID] = _generate_cart_key()
        else:
            session[settings.CART_SESSION_ID]
        session.modified = True
        cart_session = session

        # данные запроса в переменные
        phone = request.data['phone']
        order_date = request.data['order_date']
        address = request.data['address']

        if cart_session:
            if user.is_authenticated:
                delivery_info, created = DeliveryInfo.objects.get_or_create(
                    user=user,
                    type=delivery_type,
                    phone=phone,
                    order_date=order_date
                )
            else:
                delivery_info, created = DeliveryInfo.objects.update_or_create(
                    session_id=session[settings.CART_SESSION_ID],
                    defaults={
                        "type": delivery_type,
                        "phone": phone,
                        "order_date": order_date
                    }
                )
                # address_obj, address_created = Address.objects.update_or_create(
                #     defaults={
                #         "city": address["city"],
                #         "region": address["region"],
                #         "street": address["street"],
                #         "building": address["building"],
                #         "office": address["office"],
                #         "floor": address["floor"],
                #         "latitude": address["latitude"],
                #         "longitude": address["longitude"]
                #     }
                # )

        return Response({"detail": delivery_info})

        # serializer = DeliveryInfoSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(type=delivery_type)
        #     if user.is_authenticated:
        #         serializer.save(user=user,
        #                         type=delivery_type)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)

