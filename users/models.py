import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    job = models.CharField(max_length=200, default="O'qituvchi", blank=True, null=True)
    profile_picture = models.ImageField(upload_to='thedevu101-admin-media/profile-pictures/',
                                        null=True,
                                        blank=True,
                                        default='profile-pictures/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    USERNAME_FIELD = 'email'

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = (
            ('first_name', 'last_name'),
        )
