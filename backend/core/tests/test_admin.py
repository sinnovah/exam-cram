"""
Unit tests for Django admin modifications.
"""
from django.test import TestCase, Client
from django.urls import reverse

from core.tests.helpers import create_user, create_superuser


class AdminTests(TestCase):
    """Test suite for the admin panel."""

    def setUp(self):
        """Set up the test suite."""

        # Create a test client to make http requests
        self.client = Client()

        # Create a superuser
        self.superuser = create_superuser()

        # Log the superuser in with forced authentication
        self.client.force_login(self.superuser)

        # Create a standard user
        self.user = create_user(first_name='Test', last_name='User')

    def test_list_users(self):
        '''Test listing users in the admin panel'''

        # Get the url for the users list
        url = reverse('admin:core_user_changelist')
        # Make a GET request to the url with logged in superuser
        response = self.client.get(url)

        # Test that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Test that the response contains the superuser's names and email
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)
