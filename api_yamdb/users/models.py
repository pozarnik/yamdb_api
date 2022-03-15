from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    'user',
    'moderator',
    'admin',
)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
