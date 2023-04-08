from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.que.models import Que
from apps.que.models.enums.que_status import QueStatus
from apps.que.serializers import QueSerializer


class QueueScreenAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Que.objects.filter(
            order__institution_id=institution.id,
            status__in=[QueStatus.COOKING, QueStatus.READY]
        ).order_by("position")
        serializer = QueSerializer(query, many=True)
        return Response(serializer.data)
