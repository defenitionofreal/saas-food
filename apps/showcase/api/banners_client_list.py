from rest_framework.views import APIView
from rest_framework.response import Response

from apps.company.models import Institution
from apps.company.models import Banner
from apps.company.serializers import BannerSerializer


class BannersClientListAPIView(APIView):

    def get(self, request, domain):
        institution = Institution.objects.get(domain=domain)
        query = Banner.objects.filter(institution=institution,
                                       is_active=True).order_by('row')
        serializer = BannerSerializer(query, many=True)
        return Response(serializer.data)
