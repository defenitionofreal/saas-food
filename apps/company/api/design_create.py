from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.company.serializers import DesignSerializer
from apps.company.models import Institution
from apps.company.services.compare_institution import _compare_inst


class DesignCreateAPIView(APIView):
    """ Create new design """
    permission_classes = [IsAuthenticated]

    # на фронте create or update
    def post(self, request):
        serializer = DesignSerializer(data=request.data)
        institution = Institution.objects.filter(user=self.request.user)

        if not _compare_inst(request.data["institution"],
                             institution.values_list('id', flat=True)):
            return Response({"detail": f"wrong institution id"},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
