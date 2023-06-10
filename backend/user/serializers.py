"""
Serializers for the user API view.
"""
from django.contrib.auth import get_user_model, password_validation

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object. Takes JSON, validates it,
    then and saves it to the user model.
    """

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the user model
        model = get_user_model()
        # Fields to include in the user API
        fields = ['first_name', 'last_name', 'email', 'password']
        # Extra keyword arguments passes extra metadata
        # Make password write only, i.e., password won't be in the response
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        """
        Validate the password with Django's validators
        Checks if the password is less than 8 characters
        Checks if the password is too common
        Checks if the password is entirely numeric
        """

        # Validate the password against Django's validators
        password_validation.validate_password(password)
        # Return the validated password
        return password

    def create(self, validated_data):
        """Create a new valid user and return it"""

        # Create a user if the validation of the data was a success
        return get_user_model().objects.create_user(**validated_data)
