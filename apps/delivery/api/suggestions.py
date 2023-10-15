from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.delivery.services.geocoder import KladrSuggestions

import os


class KladrSuggestionsAPIView(APIView):

    # permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        query = request.data.get("query", None)
        kladr = KladrSuggestions(os.environ.get("KLADR_API_KEY"))
        res = kladr.suggestions(query)
        return Response(res, status=status.HTTP_200_OK)
