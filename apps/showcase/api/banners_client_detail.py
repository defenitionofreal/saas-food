from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.company.models import Institution
from apps.company.models import Banner
from apps.company.serializers import BannerSerializer


class BannersClientDetailAPIView(APIView):

    def get(self, request, domain, pk):
        institution = Institution.objects.get(domain=domain)
        query = get_object_or_404(Banner.objects, institution=institution,
                                  pk=pk)
        serializer = BannerSerializer(query)
        return Response(serializer.data)
