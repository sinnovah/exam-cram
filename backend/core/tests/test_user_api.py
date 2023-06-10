"""
Unit tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import create_user

# User API URL endpoint constants
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


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
        # Get the user the database with the email passed from payload
        user = get_user_model().objects.get(email=self.payload['email'])

        # Test that the user's password is correct
        self.assertTrue(user.check_password(self.payload['password']))
        # Test that the key password is not returned in the response
        self.assertNotIn('password', response.data)

        # Get the user's stored hashed password
        # Let Django handle the password hashing
        stored_password = user.password

        # Test that the stored password is not the same as the
        # password passed in the payload
        self.assertNotEqual(stored_password, self.payload['password'])

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
        # Test that the email already exists error code is returned
        self.assertEqual(
            response.data['email'][0].code, 'unique'
        )

    def test_create_user_with_invalid_email_format_error(self):
        """
        Test that trying to create a user with an invalid email format
        returns an error.
        """

        # List of invalid emails
        invalid_emails = [
            "userexamplecom",
            "user@examplecom",
            "userexample.com"
        ]

        # Loop through the invalid emails
        for invalid_email in invalid_emails:

            # Update the payload with an invalid email format
            self.payload['email'] = 'invalid_email_format'
            # Make a POST request to the create user endpoint
            response = self.client.post(CREATE_USER_URL, self.payload)

            # Test that the response is 400 BAD REQUEST
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # Test that the invalid error code is returned
            self.assertEqual(
                response.data['email'][0].code, 'invalid'
            )

    def test_create_user_with_long_email_error(self):
        """
        Test that trying to create a user with an email longer than 254
        characters returns an error.
        """

        # Update the payload with a long email
        self.payload['email'] = 'a' * 255 + '@example.com'
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the max_length error code is returned
        self.assertEqual(
            response.data['email'][0].code, 'max_length'
        )

    def test_create_user_with_an_empty_email_error(self):
        """
        Test that trying to create a user with an empty
        string email returns an error.
        """

        # Update the payload with an empty email
        self.payload['email'] = ''
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the blank error code is returned
        self.assertEqual(
            response.data['email'][0].code, 'blank'
        )

    def test_create_user_with_no_email_error(self):
        """
        Test that trying to create a user with no email
        returns an error.
        """

        # Remove the email from the payload
        self.payload.pop('email')
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the required error code is returned
        self.assertEqual(
            response.data['email'][0].code, 'required'
        )

    def test_create_user_with_short_password_error(self):
        """
        Test that trying to create a user with a password less than 8
        characters returns an error and the user is not in the database.
        """

        # Update the payload with a password less than 8 characters
        self.payload['password'] = 'short'
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the password too short error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'password_too_short'
        )

        # Check if the user exists (boolean) by trying to get the
        # user in the database with the email passed from payload
        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()

        # Test that the user does not exist (False)
        self.assertFalse(user_exists)

    def test_create_user_with_long_password_error(self):
        """
        Test that trying to create a user with a password more than 128
        characters returns an error.
        """

        # Update the payload with a password more than 128 characters
        self.payload['password'] = 'a' * 129
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the max_length error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'max_length'
        )

    def test_create_user_with_common_password_error(self):
        """
        Test that trying to create a user with
        a common password returns an error.
        """

        # Update the payload with a common password
        self.payload['password'] = 'iloveyou'
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the password too short error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'password_too_common'
        )

    def test_create_user_with_all_numeric_password_error(self):
        """
        Test that trying to create a user with an all
        numeric password returns an error.
        """

        # Update the payload with a numeric password
        self.payload['password'] = '284527272381290'
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the password entirely numeric error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'password_entirely_numeric'
        )

    def test_create_user_with_an_empty_password_error(self):
        """
        Test that trying to create a user with an empty
        string password returns an error.
        """

        # Update the payload with an empty password
        self.payload['password'] = ''
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the blank error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'blank'
        )

    def test_create_user_with_no_password_error(self):
        """
        Test that trying to create a user with no password
        returns an error.
        """

        # Remove the password from the payload
        self.payload.pop('password')
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the required error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'required'
        )

    def test_create_user_with_long_first_name_error(self):
        """
        Test that trying to create a user with a first name longer than
        150 characters returns an error.
        """

        # Update the payload with a long first name
        self.payload['first_name'] = 'a' * 151
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the max_length error code is returned
        self.assertEqual(
            response.data['first_name'][0].code, 'max_length'
        )

    def test_create_user_with_an_empty_first_name_error(self):
        """
        Test that trying to create a user with an empty
        string first name returns an error.
        """

        # Update the payload with an empty first name
        self.payload['first_name'] = ''
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test that the blank error code is returned
        self.assertEqual(
            response.data['first_name'][0].code, 'blank'
        )

    def test_create_user_with_no_first_name_error(self):
        """
        Test that trying to create a user with no first name
        returns an error.
        """

        # Remove the first name from the payload
        self.payload.pop('first_name')
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test that the required error code is returned
        self.assertEqual(
            response.data['first_name'][0].code, 'required'
        )

    def test_create_user_with_long_last_name_error(self):
        """
        Test that trying to create a user with a last name longer than
        150 characters returns an error.
        """

        # Update the payload with a long last name
        self.payload['last_name'] = 'a' * 151
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test that the max_length error code is returned
        self.assertEqual(
            response.data['last_name'][0].code, 'max_length'
        )

    def test_create_user_with_an_empty_last_name_error(self):
        """
        Test that trying to create a user with an empty
        string last name returns an error.
        """

        # Update the payload with an empty last name
        self.payload['last_name'] = ''
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test that the blank error code is returned
        self.assertEqual(
            response.data['last_name'][0].code, 'blank'
        )

    def test_create_user_with_no_last_name_error(self):
        """
        Test that trying to create a user with no last name
        returns an error.
        """

        # Remove the last name from the payload
        self.payload.pop('last_name')
        # Make a POST request to the create user endpoint
        response = self.client.post(CREATE_USER_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test that the required error code is returned
        self.assertEqual(
            response.data['last_name'][0].code, 'required'
        )

    def test_create_token_success(self):
        """Test that a token is created for valid user credentials."""

        # Create a user in the database with
        # the details in the payload
        create_user(**self.payload)

        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that the token was created successfully
        self.assertIn('token', response.data)

    def test_create_token_with_invalid_password_error(self):
        """
        Test that trying to create a token with invalid password
        returns an error.
        """

        # Create a user in the database with
        # the details in the payload
        create_user(**self.payload)

        # Update the payload with invalid password
        self.payload['password'] = 'wrong_password'
        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the token was not created
        self.assertNotIn('token', response.data)
        # Test that the authorization error code is returned
        self.assertEqual(
            response.data['non_field_errors'][0].code, 'authorization'
        )

    def test_create_token_with_an_empty_password_error(self):
        """
        Test that trying to create a token with an empty
        string password returns an error.
        """

        # Update the payload with an empty password
        self.payload['password'] = ''
        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the token was not created
        self.assertNotIn('token', response.data)
        # Test that the blank error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'blank'
        )

    def test_create_token_with_no_password_error(self):
        """
        Test that trying to create a token with no password
        returns an error.
        """

        # Remove the password from the payload
        self.payload.pop('password')
        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the token was not created
        self.assertNotIn('token', response.data)
        # Test that the required error code is returned
        self.assertEqual(
            response.data['password'][0].code, 'required'
        )

    def test_create_token_with_invalid_email_error(self):
        """
        Test that trying to create a token with invalid email
        returns an error.
        """

        # Create a user in the database with
        # the details in the payload
        create_user(**self.payload)

        # Update the payload with invalid email
        self.payload['email'] = 'notindatabase@example.com'

        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the token was not created
        self.assertNotIn('token', response.data)
        # Test that the authorization error code is returned
        self.assertEqual(
            response.data['non_field_errors'][0].code, 'authorization'
        )

    def test_create_token_with_an_empty_email_error(self):
        """
        Test that trying to create a token with an empty
        string email returns an error.
        """

        # Update the payload with an empty email
        self.payload['email'] = ''
        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the token was not created
        self.assertNotIn('token', response.data)
        # Test that the blank error code is returned
        self.assertEqual(
            response.data['email'][0].code, 'blank'
        )

    def test_create_token_with_no_email_error(self):
        """
        Test that trying to create a token with no email
        returns an error.
        """

        # Remove the email from the payload
        self.payload.pop('email')
        # Make a POST request to the create token endpoint
        response = self.client.post(TOKEN_URL, self.payload)

        # Test that the response is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test that the token was not created
        self.assertNotIn('token', response.data)
        # Test that the required error code is returned
        self.assertEqual(
            response.data['email'][0].code, 'required'
        )
