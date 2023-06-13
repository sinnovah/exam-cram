"""
Unit tests for creating and assigning Tags to topics.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import (
    create_user,
    create_topic,
    create_tag,
    topic_details_url,
    tag_details_url
)
from core.models import Topic

from topic.serializers import (
    TopicSerializer,
    TopicDetailSerializer,
    TagSerializer
)


# Topic list endpoint constant
TOPICS_URL = reverse('topic:topic-list')


class PrivateTopicTagsApiTests(TestCase):
    """
    Test suite for the topic tags (private access).
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
            'tags': [{'name': 'Test Tag'}, {'name': 'Test Tag 2'}]
        }

    def test_create_topic_with_existing_tags_successful(self):
        """
        Test creating a topic with existing tag does not duplicate the tag.
        """

        # Create an existing tag
        existing_tag = create_tag(user=self.user, name='Test Tag')
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

        # Check that the topic has two tags
        self.assertEqual(topic.tags.count(), 2)

        # Check that the topic has the existing tag
        # and not creating a duplicate tag
        self.assertIn(existing_tag, topic.tags.all())

        # Iterate over the payload's tags
        for tag in self.payload['tags']:
            # Check that the user's topic tag names
            # exist and match the payload
            self.assertTrue(
                topic.tags.filter(
                    user=self.user,
                    name=tag['name']
                ).exists()
            )
