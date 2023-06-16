"""
Database models for the project.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings
from django.core.validators import URLValidator


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


class Topic(models.Model):
    """
    Model for the topic to be studied.
    Extends Django's standard Model.
    """

    # User that the topic belongs to.
    # A user can have many topics.
    # A topic must have one user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # When a user is deleted so is their topics
        on_delete=models.CASCADE
    )
    # Topic title
    title = models.CharField(max_length=255)
    # Topic notes
    notes = models.TextField(blank=True)
    # Date and time the topic was last modified. Stores the
    # current DateTime on Topic creation and updates.
    last_modified = models.DateTimeField(auto_now=True)
    # Tags that can be allocated to topics.
    # A topic can have many tags.
    # A tag can have many topics.
    tags = models.ManyToManyField('Tag')
    # Resources that can be allocated to topics.
    # A topic can have many resources.
    # A resource can have many topics.
    resources = models.ManyToManyField('Resource')
    # Questions that can be allocated to topics.
    # A topic can have many questions.
    # A question can have many topics.
    questions = models.ManyToManyField('Question')

    def __str__(self):
        """
        Return the title as a string representation
        of the topic object.
        """

        return self.title


class Tag(models.Model):
    """
    Model for the tags that can be allocated to topics.
    Allows for topic filtering by tags.
    Extends Django's standard Model.
    """

    # Name of the tag
    name = models.CharField(max_length=255)
    # User that the tag belongs to.
    # A user can have many tags.
    # A tag must have one user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # When a user is deleted so are their tags
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Return the name as a string representation
        of the tag object.
        """

        return self.name


class Resource(models.Model):
    """
    Model for the resources that can be allocated to topics.
    Allows for topic filtering by resources.
    Extends Django's standard Model.
    """

    # Name of the resource
    name = models.CharField(max_length=255)
    # URL for the resource
    # URLValidator ensures that the URL is a valid http or https URL
    link = models.URLField(
        max_length=255,
        validators=[URLValidator(schemes=['http', 'https'])]
    )
    # User that the resource belongs to.
    # A user can have many resources.
    # A resource must have one user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # When a user is deleted so are their resources
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Return the name as a string representation
        of the resource object.
        """

        return self.name


class Question(models.Model):
    """
    Model for the questions that can be allocated to topics.
    Allows for topic filtering by questions.
    Extends Django's standard Model.
    """

    # Name of the question (question itself)
    name = models.CharField(max_length=255)
    # Answer to the question
    answer = models.CharField(max_length=255)
    # User that the question belongs to.
    # A user can have many questions.
    # A question must have one user.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # When a user is deleted so are their questions
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Return the name as a string representation
        of the question object.
        """

        return self.name
