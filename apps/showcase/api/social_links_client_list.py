from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import SocialLinks
from apps.company.serializers import SocialLinksSerializer


class SocialLinksClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = SocialLinks.objects.filter(institution=institution)
        serializer = SocialLinksSerializer(query, many=True)
        return Response(serializer.data)
