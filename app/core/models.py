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
        Creates, saves, and returns a user. extra_fields can be used
        to add additional fields to the user model automatically.
        '''
        # Check if email was not provided
        if not email:
            # Raise a ValueError exception
            raise ValueError('User must have an email address')
        # Associate model with manager, normalize the user's email value
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Password defaults to None which makes an unusable user which
        # is helpful for testing user access (based off default Django model).
        # set_password encrypts the password
        user.set_password(password)
        # Save user to database
        user.save(using=self._db)
        # Return user object
        return user

    def create_superuser(self, email, password):
        """Creates, saves, and returns a new superuser"""

        # Create a standard user with create_user method
        superuser = self.create_user(email, password)
        # Set user as superuser and staff
        superuser.is_staff = True
        superuser.is_superuser = True
        # Save the superuser to database
        superuser.save(using=self._db)
        # Return user object
        return superuser


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
    # Users are not staff (admin access) by default
    # It can be changed to True to give admin access.
    is_staff = models.BooleanField(default=False)

    # Assign manager to model
    objects = UserManager()

    # Replace the default username field with email
    USERNAME_FIELD = 'email'
