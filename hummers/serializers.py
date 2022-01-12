from rest_framework import serializers, exceptions

from .models import Profile, Tweet


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Profile
        fields = ('username', 'about', 'image',)
        read_only_fields = ('username',)


class TweetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = Tweet
        fields = ('id', 'username', 'tweet', 'image')
        read_only_fields = ('username',)

    def validate_tweet(self, value):
        if len(value) < 2:
            raise exceptions.ValidationError('Tweet is too short')

        if len(value) > 25:
            raise exceptions.ValidationError('Tweet is too long')

        return value
