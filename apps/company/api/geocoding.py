import requests as r
from rest_framework.views import APIView
from rest_framework.response import Response


class GetAddressApiView(APIView):

    def get(self, request):
        params = request.query_params["address"]
        url_base = "https://nominatim.openstreetmap.org/"
        url_sets = f"search?format=json&addressdetails=1&polygon_svg=1"
        url = url_base + url_sets + f"&q={params}"
        address = r.get(url)
        if address.status_code != 200:
            return Response({"detail": "error"}, status=address.status_code)
        return Response(address.json())
