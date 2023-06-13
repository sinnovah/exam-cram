"""
Unit tests for the Tag API.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from topic.serializers import TagSerializer

from core.models import Tag
from core.tests.helpers import (
    create_user,
    create_tag,
    tag_details_url
)


# Tag list endpoint constant
TAGS_URL = reverse('topic:tag-list')


class PublicTagApiTests(TestCase):
    """Test the publicly available Tag API."""

    def setUp(self):
        """Set up the public tag API test suite."""

        # Create a public client
        self.client = APIClient()

    def test_authentication_required_for_tags(self):
        """
        Test that authentication is required for retrieving tags.
        """

        # Attempt to retrieve tags
        response = self.client.get(TAGS_URL)

        # Test that the request was not successful
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Test that the not authenticated error code is returned
        self.assertEqual(
            response.data['detail'].code, 'not_authenticated'
        )


class PrivateTopicApiTests(TestCase):
    """
    Test suite for the tag API (private access).
    Authenticated requests.
    """

    def setUp(self):
        """Set up the test suite."""

        # Create a test client to make test http requests
        self.client = APIClient()
        # Create a test user
        self.user = create_user()

        # Authenticate the test user
        self.client.force_authenticate(user=self.user)

    def test_list_tags_successful(self):
        """
        Test retrieving and listing tags for a user is successful.
        """

        # Create a test tag for the user
        create_tag(user=self.user)
        # Create a second test tag for the user
        create_tag(user=self.user, name='Test Tag 2')

        # Retrieve the two created tag
        response = self.client.get(TAGS_URL)
        # Retrieve all tags from the database
        # Order by name alphabetically
        tags = Tag.objects.all().order_by('name')
        # Serialize the tags retrieved from the database
        # Many=True because we are serializing a list of tag objects
        serializer = TagSerializer(tags, many=True)

        # Test that the get tags request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there are 2 tags in the response
        self.assertEqual(len(response.data), 2)
        # Test that the tags in the response match
        # the serialized tags from the database
        self.assertEqual(response.data, serializer.data)

    def test_list_tags_limited_to_user(self):
        """
        Test that the tags list is limited to the authenticated user.
        """

        # Create another test user
        other_user = create_user(email='other@example.com')

        # Create a test tag for the authenticated user
        create_tag(user=self.user)
        # Create a test tag for the other user
        create_tag(user=other_user, name='Test Tag 2')

        # Retrieve the tag for the authenticated user
        response = self.client.get(TAGS_URL)
        # Retrieve tags from the database
        tags = Tag.objects.filter(user=self.user)
        # Serialize the tags retrieved from the database
        # Many=True because we are serializing a list of tag objects
        serializer = TagSerializer(tags, many=True)

        # Test that the get tags request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there is 1 tag in the response
        # (1 for the authenticated user)
        self.assertEqual(len(response.data), 1)
        # Test that the tags in the response match
        # the serialized tags from the database
        self.assertEqual(response.data, serializer.data)

    def test_patch_tag_success(self):
        """
        Test patching a tag is successful.
        """

        # Create a test tag for the user
        tag = create_tag(user=self.user)
        # Set the new tag name
        payload = {'name': 'New Tag Name'}
        # URL for the tag, passing in the tag id
        url = tag_details_url(tag.id)
        # Patch the tag
        response = self.client.patch(url, payload)

        # Refresh the tag from the database
        tag.refresh_from_db()

        # Test that the patch request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that the tag name has been patched
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag_success(self):
        """
        Test deleting a tag is successful.
        """

        # Create a test tag for the user
        tag = create_tag(user=self.user)
        # URL for the tag, passing in the tag id
        url = tag_details_url(tag.id)
        # Delete the tag
        response = self.client.delete(url)

        # Test that the delete request was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Retrieve tags for the authenticated user from the database
        tags = Tag.objects.filter(user=self.user)

        # Test that the tag has been deleted (does not exist)
        self.assertFalse(tags.exists())
