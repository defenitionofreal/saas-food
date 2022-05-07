from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.company.serializers import DesignSerializer
from apps.company.models import Institution, Design
from apps.company.services.compare_institution import (_find_wrong_inst_id,
                                                       _check_duplicated_uuid)


class DesignCreateAPIView(APIView):
    """ Create new design """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DesignSerializer(data=request.data)
        institution = Institution.objects.filter(user=self.request.user)
        design = Design.objects.filter(user=self.request.user)

        data = request.data["institution"]

        if data:
            if _find_wrong_inst_id(data, institution.values_list('id',
                                                                 flat=True)):
                return Response({"detail": f"wrong institution id"},
                                status=status.HTTP_400_BAD_REQUEST)
            if _check_duplicated_uuid(data, design.values_list('institution',
                                                               flat=True)):
                return Response(
                    {"detail": f"institution already has a design"},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "institution is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
