from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import SocialLinks
from apps.company.serializers import SocialLinksSerializer


class SocialLinksAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = get_object_or_404(SocialLinks, institution=institution)
        serializer = SocialLinksSerializer(query)
        return Response(serializer.data)
