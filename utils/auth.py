import datetime

import jwt
from jwt import DecodeError

from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from django.contrib.auth import get_user_model


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }

    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }

    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_TOKEN_SECRET,
        algorithm='HS256'
    )

    return refresh_token


class UserJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Access token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except DecodeError:
            raise exceptions.ParseError('Failed to decode access token')
        except Exception:
            raise exceptions.APIException('Failed to decode access token')

        User = get_user_model()
        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        if not hasattr(user, 'chef') and not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        return (user, None)
