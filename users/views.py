from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserAuthSerializer, ConfirmSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
import random


@api_view(['POST'])
def registration_api_view(request):

    serializer = UserRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')


    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )


    code = str(random.randint(100000, 999999))
    ConfirmCode.objects.create(user=user, code=code)

    print(f'Код подтверждения для {username}: {code}')  # в реальном проекте отправляем на email

    return Response(
        status=status.HTTP_201_CREATED,
        data={'user_id': user.id, 'code': code}  # code убрать когда будет email
    )


@api_view(['POST'])
def authorization_api_view(request):
   
    serializer = UserAuthSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

 
    user = authenticate(username=username, password=password)

    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def confirm_api_view(request):

    serializer = ConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)

    code = serializer.validated_data.get('code')


    try:
        confirm = ConfirmCode.objects.get(code=code)
    except ConfirmCode.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'error': 'Wrong code!'})


    user = confirm.user
    user.is_active = True
    user.save()
    confirm.delete()

    return Response(status=status.HTTP_200_OK,
                    data={'message': 'User activated successfully!'})
