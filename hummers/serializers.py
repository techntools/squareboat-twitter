from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    about = serializers.CharField(allow_blank=True, required=False)
    image = serializers.URLField(allow_blank=False)

    class Meta:
        model = Profile
        fields = ('username', 'about', 'image',)
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
