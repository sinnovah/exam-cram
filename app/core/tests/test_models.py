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
PASSWORD = 'ThirtyHairyHippos896'


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

    def test_user_email_normalized(self):
        '''
        Test that emails for new users are normalized
        '''

        # List of input emails and expected normalized output emails
        # As per email spec:
        # Everything before the @ symbol should retain case
        # Everything after the @ symbol should be lowercase
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        # Loop through the sample emails
        for input_email, output_email in sample_emails:
            # Create the user
            user = Helpers.create_user(email=input_email)
            # Test that the user's email was normalized successfully
            self.assertEqual(user.email, output_email)

    def test_empty_user_email_raises_error(self):
        '''Test that creating a user without an email raises a ValueError'''

        # Test that a ValueError exception is raised
        with self.assertRaises(ValueError):
            # Create the user with an empty, invalid email
            Helpers.create_user(email='')
