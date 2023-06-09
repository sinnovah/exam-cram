"""
User API views.
"""
from rest_framework import generics

from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """
    View for the user API to create a new
    user. Extends DRF's API view.
    """

    # Set DRF's serializer class to the custom user serializer
    serializer_class = UserSerializer
