"""
Unit tests for models.
"""
from django.test import TestCase
# Use get_user_model to access the custom user model
# Allows for a change to the default user model
# from django.contrib.auth import get_user_model

from core.tests import test_helpers as Helpers

# Default values of create-user helper function
USER = 'user@example.com'
PASSWORD = 'testpass123'


class ModelTests(TestCase):
    """Test suite for the models in the project."""

    def test_create_user_with_email_success(self):
        """Test creating a new user with an email is successful."""

        # Create the user
        user = Helpers.create_user()

        # Test that the user's email was created successfully
        self.assertEqual(user.email, USER)
        # Test that the user's password was created successfully
        # check_password checks the hashed password
        self.assertTrue(user.check_password, PASSWORD)
