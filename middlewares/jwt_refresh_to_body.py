from django.utils.deprecation import MiddlewareMixin
import json


class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token/refresh"
    endpoint --- check for a 'refresh' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # print(request.path)
        if request.path == '/api/organization/token/refresh/' and 'refresh' in request.COOKIES:
            if request.body != b'':
                data = json.loads(request.body)
                data['refresh'] = request.COOKIES['refresh']
                request._body = json.dumps(data).encode('utf-8')
            else:
                pass

        return None
