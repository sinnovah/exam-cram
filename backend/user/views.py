"""
User API views.
"""
from rest_framework import generics, authentication, permissions
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
    Requires valid login credentials to generate a token.
    """
    # Extends DRF's ObtainAuthToken view.

    # Set DRF's serializer class to the custom token serializer
    serializer_class = TokenSerializer
    # Enable the browsable UI for the token API endpoint
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Endpoint to manage the authenticated user [GET, PUT, PATCH].
    """
    # Extends DRF's RetrieveUpdateAPIView.

    # Set DRF's serializer class to the custom user serializer
    serializer_class = UserSerializer

    # Set the authentication and permission classes
    # to the default DRF classes
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the authenticated user
        """

        # Return the authenticated user
        return self.request.user
