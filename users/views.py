from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import AuthToken

from .models import Address, User

from .serializers import AddressSerializer, UserSerializer, RegisterSerializer, LoginSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serialized_user = UserSerializer(user, context=self.get_serializer_context()).data,
        serialized_address  = ''
        if user.address:
            address = Address.objects.get(pk=serialized_user[0]['address'])
            serialized_address = AddressSerializer(address).data

        _, token = AuthToken.objects.create(user)
        return Response({
            'user': serialized_user[0],
            'address': serialized_address,
            'token': token
        })


class UserAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user