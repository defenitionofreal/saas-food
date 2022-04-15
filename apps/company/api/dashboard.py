from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        if user.is_authenticated and not user.is_customer:
            return Response({"detail": "success",
                             "user_id": user.id,
                             "user_phone": str(user.phone)}, status=200)
        return Response({"detail": "fail"}, status=400)
