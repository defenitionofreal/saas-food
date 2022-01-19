from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

from apps.base.authentication import JWTAuthentication

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginAPIView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect password")

        if 'api/customer' in request.path:
            scope = 'customer'
        elif 'api/organization' in request.path:
            scope = 'organization'

        if user.is_customer and scope == 'api/organization':
            raise exceptions.AuthenticationFailed('Unauthorized')

        token = JWTAuthentication.generate_jwt(user.id, scope)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': "success"
        }
        return response
