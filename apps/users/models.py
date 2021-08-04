"""
User model
"""
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
 
        user.is_admin = True
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser):
    """
    User model
    Extends Django's Abstract Base User

    Auto generated fields:
        - id
        - last_login
        - password
    
    Register/Login fields:
        - email
        - password
    """
    email = models.EmailField(max_length=255, unique=True)

    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Other than pass and email(USERNAME_FIELD)

    def __str__(self):
        return self.email
