"""
User API views.
"""
from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create user, publicly available API endpoint [POST].
    """
    # Extends DRF's API view.

    # Set DRF's serializer class to the custom user serializer
    serializer_class = UserSerializer
