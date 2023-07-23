from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import Requisites
from apps.company.serializers import RequisitesSerializer


class RequisitesAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = get_object_or_404(Requisites, institutions=institution)
        serializer = RequisitesSerializer(query)
        return Response(serializer.data)
