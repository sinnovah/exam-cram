"""
User API views.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    TokenSerializer
)


class CreateUserView(generics.CreateAPIView):
    """
    Create user, publicly available API endpoint [POST].
    """
    # Extends DRF's API view.

    # Set DRF's serializer class to the custom user serializer
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Token API endpoint for user authentication [POST].
    """
    # Extends DRF's ObtainAuthToken view.

    # Set DRF's serializer class to the custom token serializer
    serializer_class = TokenSerializer
    # Enable the browsable UI for the token API endpoint
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
