"""
Serializers for the user API view.
"""
from django.contrib.auth import (
    get_user_model,
    password_validation,
    authenticate
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User object. first_name, last_name,
    email, and password fields.
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

    def update(self, instance, validated_data):
        """Update a user with encrypted password correctly and return it"""

        # Get the password from the validated data
        # If the password is not provided, return None
        password = validated_data.pop('password', None)
        # Update the user with the validated data
        # with existing update method from ModelSerializer
        user = super().update(instance, validated_data)

        # If a password was provided
        if password:
            # Set the password (encrypts it)
            user.set_password(password)
            # Save the user to the database
            user.save()

        # Return the user
        return user


class TokenSerializer(serializers.Serializer):
    """
    Token object for user authentication. Requires valid
    email and password credentials to generate the token.
    """

    # Fields for authentication with the token API
    email = serializers.EmailField()
    password = serializers.CharField(
        # Hide the password
        style={'input_type': 'password'},
        # Retain spaces in the password
        trim_whitespace=False
    )

    # Validate the email and password when the serializer is called by view
    def validate(self, attrs):
        """Validate and authenticate the user that is logging in"""

        # Get the email and password from the request
        email = attrs.get('email')
        password = attrs.get('password')
        # Authenticate the user with the provided credentials
        user = authenticate(
            request=self.context.get('request'),
            username=email,  # Use email instead of username
            password=password
        )

        # If the authentication failed
        if not user:
            # Set the error message
            msg = _('Unable to authenticate with provided credentials.')
            # Raise a validation error
            raise serializers.ValidationError(msg, code='authorization')

        # Set the user attribute
        attrs['user'] = user
        # Return the validated attributes
        return attrs
