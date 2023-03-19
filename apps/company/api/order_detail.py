from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.order.models import Cart


class OrderDetailAPIView(APIView):
    """
    Retrieve, update or delete a order instance.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, order_pk):
        order = get_object_or_404(Cart.objects,
                                  institution__user=self.request.user,
                                  pk=order_pk)
        serializer = None
        return Response(serializer.data)

    def put(self, request, order_pk):
        """
        Change only status and paid fields!
        """
        order = get_object_or_404(Cart.objects,
                                  institution__user=self.request.user,
                                  pk=order_pk)
        serializer = None
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_pk):
        order = get_object_or_404(Cart.objects,
                                  institution__user=self.request.user,
                                  pk=order_pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
