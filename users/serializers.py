from rest_framework.serializers import ModelSerializer, Serializer, CharField, ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import Address, User


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['zip_code', 'state', 'city', 'neighborhood', 'street', 'house_number', 'complement']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'cpf', 'image', 'address']


class RegisterSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'cpf']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            cpf=validated_data['cpf'],
        )
        return user


class LoginSerializer(Serializer):
    email = CharField()
    password = CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise ValidationError('Incorrect Credentials')


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)    

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UpdateUserSerializer(Serializer):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    cpf = CharField(required=True)


class UpdateAddressSerializer(Serializer):
    zip_code = CharField(required=True)
    state = CharField(required=True)
    city = CharField(required=True)
    neighborhood = CharField(required=True)
    street = CharField(required=True)
    house_number = CharField(required=True)
    complement = CharField(required=True)