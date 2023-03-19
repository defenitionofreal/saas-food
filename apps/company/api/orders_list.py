from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.order.models import Cart

#TODO: филтры и сортировки
class OrderListAPIView(APIView):
    """ List orders """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Cart.objects.filter(institution__user=self.request.user)\
            .select_related("institution")
        serializer = None
        return Response(serializer.data)
