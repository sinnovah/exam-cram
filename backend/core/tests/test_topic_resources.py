"""
Unit tests for creating and assigning resources to topics.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import (
    create_user,
    create_resource,
    create_topic,
    topic_details_url
)
from core.models import Topic, Resource


# Topic list endpoint constant
TOPICS_URL = reverse('topic:topic-list')


class PrivateTopicResourcesApiTests(TestCase):
    """
    Test suite for the topic resources (private access).
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

        # Topic data to send to endpoints
        self.payload = {
            'title': 'Test Topic',
            'notes': 'Test notes for my topic',
            'resources': [
                {'name': 'Test Resource', 'link': 'https://example.com'},
                {'name': 'Test Resource 2', 'link': 'http://example.com'}
            ]
        }

    def test_create_topic_with_existing_resources_successful(self):
        """
        Test creating a topic with existing
        resource does not duplicate the resource.
        """

        # Create an existing resource
        existing_resource = create_resource(
            user=self.user,
            name='Test Resource'
        )
        # Post the payload with the same tag name as the existing tag
        result = self.client.post(TOPICS_URL, self.payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # Get the user's topics from the database
        topics = Topic.objects.filter(user=self.user)

        # Check that there is one topic
        self.assertEqual(topics.count(), 1)

        # Get the first and only topic from the queryset
        topic = topics[0]

        # Check that the topic has two resources
        self.assertEqual(topic.resources.count(), 2)

        # Check that the topic has the existing resource
        # and not creating a duplicate resource
        self.assertIn(existing_resource, topic.resources.all())

        # Iterate over the payload's resources
        for resource in self.payload['resources']:
            # Check that the user's topic resources names
            # and links exist and match the payload
            self.assertTrue(
                topic.resources.filter(
                    user=self.user,
                    name=resource['name'],
                    link=resource['link']
                ).exists()
            )

    def test_create_resource_on_topic_patch(self):
        """
        Test creating a new resource when patching a topic.
        """

        # Create a topic
        topic = create_topic(user=self.user)
        # Create a payload with a different resource name
        payload = {'resources': [{'name': 'Different Resource'}]}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Update the topic details with the different resource payload
        result = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the topic has one resource
        self.assertEqual(topic.resources.count(), 1)

        # Get the new resource from the database
        new_resource = Resource.objects.get(name='Different Resource')

        # Check that the topic has the new resource
        self.assertIn(new_resource, topic.resources.all())

    def test_patch_topic_by_assigning_existing_resource(self):
        """
        Test patching a topic by assigning existing resources.
        """

        # Create an original resource
        original_resource = create_resource(user=self.user)
        # Create a topic
        topic = create_topic(user=self.user)

        # Add the original_resource to the topic
        topic.resources.add(original_resource)

        # Create a different resource
        different_resource = create_resource(
            user=self.user, name='Different Resource'
        )
        # Create a payload with the existing resource's name
        # to change the topic's resource to the different resource
        payload = {'resources': [{'name': 'Different Resource'}]}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Update the topic details with the different resource from the payload
        result = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the topic has one resource
        self.assertEqual(topic.resources.count(), 1)
        # Check that the topic has the different resource
        self.assertIn(different_resource, topic.resources.all())
        # Check that the topic does not have the original resource
        # because it has been replaced by the different resource
        self.assertNotIn(original_resource, topic.resources.all())

    def test_clear_topic_resources(self):
        """
        Test clearing a topic's resources.
        """

        # Create a topic
        topic = create_topic(user=self.user)
        # Create a resource
        resource = create_resource(user=self.user)
        # Add the resource to the topic
        topic.resources.add(resource)

        # Create a payload with no resources
        payload = {'resources': []}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Update the topic details with the payload
        result = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the topic has no resources
        self.assertEqual(topic.resources.count(), 0)
