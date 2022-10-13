from rest_framework.viewsets import ModelViewSet

from .models import Address, User

from .serializers import AddressSerializer, UsersSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
