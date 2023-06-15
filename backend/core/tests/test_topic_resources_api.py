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
)
from core.models import Topic


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
