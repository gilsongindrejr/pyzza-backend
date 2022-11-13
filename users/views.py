from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from knox.auth import AuthToken

from .models import Address, User

from .serializers import AddressSerializer, UserSerializer, RegisterSerializer, LoginSerializer, ChangePasswordSerializer, UpdateUserSerializer, UpdateAddressSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serialized_user = UserSerializer(
            user, context=self.get_serializer_context()).data,
        serialized_address = ''
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
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordAPI(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({'old_password': ['Wrong password.']}, status=HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpdateUserAndAddressAPI(GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'cpf': request.data.get('cpf'),
        }
        user_serializer = UpdateUserSerializer(data=user_data)

        address = None
        errors = []

        if user.address:
            address = Address.objects.get(pk=user.address.id)
            address_data = {
                'zip_code': request.data.get('zip_code'),
                'state': request.data.get('state'),
                'city': request.data.get('city'),
                'neighborhood': request.data.get('neighborhood'),
                'street': request.data.get('street'),
                'house_number': request.data.get('house_number'),
                'complement': request.data.get('complement')
            }
            address_serializer = UpdateAddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address.zip_code = address_serializer.data.get('zip_code')
                address.state = address_serializer.data.get('state')
                address.city = address_serializer.data.get('city')
                address.neighborhood = address_serializer.data.get('neighborhood')
                address.street = address_serializer.data.get('street')
                address.house_number = address_serializer.data.get('house_number')
                address.complement = address_serializer.data.get('complement')
                address.save()
            else: 
                errors.append(address_serializer.errors)

        if user_serializer.is_valid():
            user.first_name = user_serializer.data.get('first_name')
            user.last_name = user_serializer.data.get('last_name')
            user.cpf = user_serializer.data.get('cpf')
            user.save()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            errors.append(user_serializer.errors)
        
        return Response(errors, status=HTTP_400_BAD_REQUEST)
