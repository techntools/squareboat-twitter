from django.shortcuts import get_object_or_404

from django.conf import settings

from rest_framework import generics, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

import jwt

from accounts.serializers import UserSerializer

from accounts.models import User

from utils.auth import generate_access_token, generate_refresh_token


class Create(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class Profile(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(pk=self.request.user.id)

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            raise exceptions.NotAuthenticated()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        if not user.check_password(request.data.get('password')):
            raise exceptions.NotAuthenticated('Wrong password')

        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response()

        response.set_cookie(
            key='refreshtoken',
            value=refresh_token,
            httponly=True
        )

        data = {
            'access_token': access_token,
            **serialized_user
        }

        response.data = data

        return response


class NewAccessToken(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            raise exceptions.NotAuthenticated('Missing refresh token')

        try:
            payload = jwt.decode(
                refresh_token,
                settings.REFRESH_TOKEN_SECRET,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.NotAuthenticated('Refresh token has expired')

        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        access_token = generate_access_token(user)

        return Response({ 'access_token': access_token })
