"""
Unit tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import create_user

# User API URL constants
CREATE_USER_URL = reverse('user:create')


class PublicUserApiTests(TestCase):
    """Test suite for the user API (public access)."""

    def setUp(self):
        """Set up the test suite."""

        # Create a test client to make test http requests
        self.client = APIClient()
        # Payload for user API requests
        self.payload = {
            'email': 'user@example.com',
            'password': 'ThirtyHairyHippos896',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user_success(self):
        """Test creating a user is successful."""

        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test that the user was created successfully
        # Get the user  the database with the email passed from payload
        user = get_user_model().objects.get(email=self.payload['email'])

        # Test that the user's password is correct
        self.assertTrue(user.check_password(self.payload['password']))
        # Test that the key password is not returned in the response
        self.assertNotIn('password', response.data)

    def test_create_user_with_email_exists_error(self):
        """
        Test that trying to create a user with an email that already exists
        in the database returns a  400 bad request message in the response.
        """

        # Create a user in the database with
        # the details in the payload
        create_user(**self.payload)

        # Make a POST request to the create user endpoint with the
        # same user details, including the email address
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password_error(self):
        """
        Test that trying to create a user with a password less than
        8 characters returns a 400 bad request message in the response
        and the user is not saved in the database.
        """

        # Update the payload with a password less than 8 characters
        self.payload['password'] = 'short'

        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check if the user exists (boolean) by getting the user in
        # the database with the email passed from payload
        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()

        # Test that the user does not exist (False)
        self.assertFalse(user_exists)
