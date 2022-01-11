from django.db import models
from django.contrib.auth import get_user_model

from utils.models import EntryTimestamp


class Profile(EntryTimestamp):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE
    )
    about = models.TextField(blank=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.user.username


class Followers(models.Model):
    follower = models.ForeignKey(
        get_user_model(),
        related_name='following',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        get_user_model(),
        related_name='followers',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_followers')
        ]

        ordering = ['-created_at']

        def __str__(self):
            return f'{self.follower} follows {self.following}'
