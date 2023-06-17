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
    create_topic,
    resource_details_url
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

    def test_patch_resource_success(self):
        """
        Test patching a resource is successful.
        """

        # Create a test resource for the user
        resource = create_resource(user=self.user)
        # Set the new resource name
        payload = {'name': 'New Resource Name'}
        # URL for the resource, passing in the resource id
        url = resource_details_url(resource.id)
        # Patch the resource
        response = self.client.patch(url, payload)

        # Retrieve the updated resource from the database
        resource.refresh_from_db()

        # Test that the patch request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that the resource name has been patched
        self.assertEqual(resource.name, payload['name'])

    def test_delete_resource_success(self):
        """
        Test deleting a resource is successful.
        """

        # Create a test resource for the user
        resource = create_resource(user=self.user)
        # URL for the resource, passing in the resource id
        url = resource_details_url(resource.id)
        # Delete the resource
        response = self.client.delete(url)

        # Test that the delete request was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Retrieve the resource from the database
        resource = Resource.objects.filter(user=self.user, id=resource.id)

        # Test that the resource has been deleted
        self.assertFalse(resource.exists())

    def test_filter_resources_by_those_assigned_to_topics(self):
        """
        Test filtering resources by those assigned to topics.
        """

        # Create resources for the user
        resource1 = create_resource(user=self.user, name='Resource 1')
        resource2 = create_resource(user=self.user, name='Resource 2')
        # Create a test topic for the user
        topic = create_topic(user=self.user, name='Test Topic')
        # Assign resource1 to the topic
        topic.resources.add(resource1)

        # Retrieve the resources assigned to the topic
        # URL for the resources list, passing in the assigned_only query param
        response = self.client.get(RESOURCES_URL, {'assigned_only': 1})

        # Serialize the resources retrieved from the database
        serializer1 = ResourceSerializer(resource1)
        serializer2 = ResourceSerializer(resource2)

        # Test that the get resources request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there is 1 resource in the response
        self.assertEqual(len(response.data), 1)
        # Test that resource1 is in the response data
        self.assertIn(serializer1.data, response.data)
        # Test that resource2 is not in the response data
        self.assertNotIn(serializer2.data, response.data)

    def test_filter_resources_by_those_assigned_unique(self):
        """
        Test filtering resources by those assigned to
        topics returns unique items.
        """

        # Create resources for the user
        resource1 = create_resource(user=self.user, name='Resource 1')
        resource2 = create_resource(user=self.user, name='Resource 2')
        # Create a test topic for the user
        topic1 = create_topic(user=self.user, name='Test Topic 1')
        # Create a second test topic for the user
        topic2 = create_topic(user=self.user, name='Test Topic 2')

        # Assign resource1 to both topics
        topic1.resources.add(resource1)
        topic2.resources.add(resource1)

        # Retrieve the resources assigned to topic1
        # URL for the resources list, passing in the assigned_only query param
        response = self.client.get(RESOURCES_URL, {'assigned_only': 1})

        # Test that the get resources request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there is 1 resource in the response
        self.assertEqual(len(response.data), 1)
        # Test that resource1 is in the response data
        self.assertEqual(response.data[0]['name'], resource1.name)
        # Test that resource2 is not in the response data
        self.assertNotEqual(response.data[0]['name'], resource2.name)
