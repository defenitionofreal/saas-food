from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'phone',
            'is_customer', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = str(user.phone)
        token['email'] = user.email
        return token


class AuthSendCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)


class AuthPhoneSerializer(AuthSendCodeSerializer):
    code = serializers.CharField(required=True)

    # def create(self, validated_data):
    #     raise AttributeError("Serializer can't create instance")
    #
    # def update(self, instance, validated_data):
    #     raise AttributeError("Serializer can't update instance")
