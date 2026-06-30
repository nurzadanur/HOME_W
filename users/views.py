import random

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmationCode, CustomUser
from .serializers import UserRegisterSerializer, UserAuthSerializer, ConfirmSerializer


class RegistrationAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        phone_number = serializer.validated_data.get('phone_number')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            is_active=False,
        )

        code = str(random.randint(100000, 999999))
        ConfirmationCode.objects.create(user=user, code=code)

        print(f'Код подтверждения для {email}: {code}')

        return Response(
            status=status.HTTP_201_CREATED,
            data={'user_id': user.id, 'code': code}
        )


class AuthorizationAPIView(GenericAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response(status=status.HTTP_401_UNAUTHORIZED, data={'error': 'Неверный email или пароль'})


class ConfirmAPIView(GenericAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        user_id = serializer.validated_data.get('user_id')
        code = serializer.validated_data.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User не найден'})

        try:
            confirm = ConfirmationCode.objects.get(user=user, code=code)
        except ConfirmationCode.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Неверный код!'})

        user.is_active = True
        user.save()
        confirm.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'User activated successfully!'})