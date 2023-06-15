"""
Unit tests for the Resource API.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from topic.serializers import ResourceSerializer

from core.models import Resource
from core.tests.helpers import (
    create_user,
    create_resource,
)


# Resource list endpoint constant
RESOURCES_URL = reverse('topic:resource-list')


class PublicResourceApiTests(TestCase):
    """Test suite for the publicly available Resource API."""

    def setUp(self):
        """Set up the public tag API test suite."""

        # Create a public client
        self.client = APIClient()

    def test_authentication_required_for_resources(self):
        """
        Test that authentication is required for retrieving resources.
        """

        # Attempt to retrieve resources
        response = self.client.get(RESOURCES_URL)

        # Test that the request was not successful
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Test that the not authenticated error code is returned
        self.assertEqual(
            response.data['detail'].code, 'not_authenticated'
        )


class PrivateResourceApiTests(TestCase):
    """
    Test suite for the resource API (private access).
    Authenticated requests.
    """

    def setUp(self):
        """Set up the test suite."""

        # Create a test client to make test http requests
        self.client = APIClient()
        # Create a test user
        self.user = create_user()

        # Authenticate the test user
        self.client.force_authenticate(self.user)

    def test_list_resources_successful(self):
        """
        Test retrieving and listing resources for a user is successful.
        """

        # Create a test resource for the user
        create_resource(user=self.user)
        # Create a second test resource for the user
        create_resource(user=self.user, name='Test Resource 2')

        # Retrieve the two created resources
        response = self.client.get(RESOURCES_URL)
        # Retrieve all resources from the database
        # Order by name alphabetically
        resources = Resource.objects.all().order_by('name')
        # Serialize the resources retrieved from the database
        # Many=True because we are serializing a list of resource objects
        serializer = ResourceSerializer(resources, many=True)

        # Test that the get resources request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there are 2 resources in the response
        self.assertEqual(len(response.data), 2)
        # Test that the resources in the response match
        # the serialized resources from the database
        self.assertEqual(response.data, serializer.data)

    def test_list_resources_limited_to_user(self):
        """
        Test that the resources list is limited to the authenticated user.
        """

        # Create another test user
        other_user = create_user(email='other@example.com')
        # Create a test resource for the other user
        create_resource(user=other_user, name='Test Resource 2')

        # Create a test resource for the authenticated user
        resource = create_resource(user=self.user)

        # Retrieve the resource for the authenticated user
        response = self.client.get(RESOURCES_URL)

        # Test that the get resources request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there is 1 resource in the response
        # (1 for the authenticated user)
        self.assertEqual(len(response.data), 1)
        # Test that the resource in the response matches
        # the authenticated user's resource from the database
        self.assertEqual(response.data[0]['name'], resource.name)
        self.assertEqual(response.data[0]['link'], resource.link)
        self.assertEqual(response.data[0]['id'], resource.id)
