"""
User model
"""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser to extend django's current user
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
