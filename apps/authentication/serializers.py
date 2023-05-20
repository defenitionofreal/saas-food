from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = str(user.phone) # ?
        token['email'] = user.email
        return token
