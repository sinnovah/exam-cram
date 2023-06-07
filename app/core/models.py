"""
Database models for the project.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    Custom user manager that supports using email instead of username.
    Extends Django's BaseUserManager.
    """

    def create_user(self, email, password=None, **extra_fields):
        '''
        Creates, saves, and returns user. extra_fields can be used
        to add additional fields to the user model automatically.
        '''

        # Associate model with manager
        user = self.model(email=email, **extra_fields)
        # Password defaults to None which makes an unusable user which
        # is helpful for testing user access (based off default Django model).
        # set_password encrypts the password
        user.set_password(password)
        # Save user to database
        user.save(using=self._db)
        # Return user object
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    Extends Django's AbstractBaseUser and PermissionsMixin.
    """

    # Email must be unique in the database for authentication
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    # Users are active by default, but can be deactivated.
    is_active = models.BooleanField(default=True)
    # Users are not staff with admin access by default
    # It can be changed to True to give admin access.
    is_staff = models.BooleanField(default=False)

    # Assign manager to model
    objects = UserManager()

    # Replace the default username field with email
    USERNAME_FIELD = 'email'
