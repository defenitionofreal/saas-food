from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.company.models import Banner, Institution
from apps.company.serializers import BannerSerializer
from apps.base.authentication import JWTAuthentication


class BannerListAPIView(APIView):
    """ List banners """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        institution = Institution.objects.get(pk=pk)
        query = Banner.objects.filter(institution=institution)
        serializer = BannerSerializer(query, many=True)
        return Response(serializer.data)
