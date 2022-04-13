from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CheckCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        if user.is_authenticated and user.is_customer:
            return Response({"detail": "success"})
        return Response({"detail": "fail"})
