from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    GenericAPIView
)

from hummers.models import Profile, Followers
from hummers.serializers import ProfileSerializer

User = get_user_model()


class HummerProfile(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProfileSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get('username', None)

        if username is None:
            username = self.request.user.username

        return Profile.objects.select_related('user').filter(
            user__username=username
        )

    def get_object(self):
        return get_object_or_404(self.get_queryset())


class Follow(GenericAPIView):
    def post(self, *arg, **kwargs):
        try:
            following_user = User.objects.get(username=self.kwargs['username'])

            Followers.objects.create(
                follower=self.request.user,
                following=following_user
            )
        except User.DoesNotExist:
            raise exceptions.NotFound('No such hummer to follow')
        except IntegrityError:
            raise exceptions.NotFound('You are already following this hummer')

        return Response()


class Unfollow(GenericAPIView):
    def post(self, *arg, **kwargs):
        try:
            following_user = User.objects.get(username=self.kwargs['username'])

            deleted = Followers.objects.filter(following=following_user).delete()
            if deleted[0] == 0:
                raise exceptions.NotFound('You are not following the hummer')
        except User.DoesNotExist:
            raise exceptions.NotFound('No such hummer to unfollow')

        return Response()
