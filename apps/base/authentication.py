import jwt, datetime
from project.settings import default

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        is_customer = 'api/customer' in request.path

        token = request.COOKIES.get('jwt')
        if not token:
            return None
        try:
            payload = jwt.decode(token, default.SECRET_KEY,
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("unauthenticated")

        if (is_customer and payload['scope'] == 'organization') or (
                not is_customer and payload['scope'] == 'customer'):
            raise exceptions.AuthenticationFailed('Invalid scope')

        user = User.objects.get(pk=payload['user_id'])
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")
        return (user, None)

    @staticmethod
    def generate_jwt(id, scope):
        payload = {
            'user_id': str(id),
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }

        return jwt.encode(payload, default.SECRET_KEY, algorithm='HS256')
