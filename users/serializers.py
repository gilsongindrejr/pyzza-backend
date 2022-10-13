from rest_framework.serializers import ModelSerializer

from .models import Address, User


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['zip_code', 'state', 'city', 'neighborhood', 'street', 'house_number', 'complement']


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        