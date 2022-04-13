from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.company.serializers import WorkingHoursSerializer
from apps.company.models import Institution


class WorkingHoursCreateAPIView(APIView):
    """ Create new working hours """
    permission_classes = [IsAuthenticated]

    # TODO:на фронте или на беке нужно сделать так,
    #  что максимум можно создать 7 объектов
    #  и чтобы choiсes не повторялись
    def post(self, request, pk):
        serializer = WorkingHoursSerializer(data=request.data)
        institution = Institution.objects.get(pk=pk)
        if serializer.is_valid():
            serializer.save(institution=institution)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
