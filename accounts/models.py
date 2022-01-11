from django.contrib.auth.models import AbstractUser

from utils.models import EntryTimestamp


class User(AbstractUser, EntryTimestamp):
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)
