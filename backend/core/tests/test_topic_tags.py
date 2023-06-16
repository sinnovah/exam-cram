"""
Unit tests for creating and assigning Tags to topics.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import (
    create_user,
    create_tag,
    create_topic,
    topic_details_url
)
from core.models import Topic, Tag


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

    def test_create_tag_on_topic_patch(self):
        """
        Test creating a new tag when patching a topic.
        """

        # Create a topic
        topic = create_topic(user=self.user)
        # Create a payload with a different tag name
        payload = {'tags': [{'name': 'Different Tag'}]}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Update the topic details with the different tag payload
        result = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the topic has one tag
        self.assertEqual(topic.tags.count(), 1)

        # Get the new tag from the database
        new_tag = Tag.objects.get(name='Different Tag')

        # Check that the topic has the new tag
        self.assertIn(new_tag, topic.tags.all())

    def test_patch_topic_by_assigning_existing_tag(self):
        """
        Test patching a topic by assigning existing tags.
        """

        # Create an original tag
        original_tag = create_tag(user=self.user)
        # Create a topic
        topic = create_topic(user=self.user)

        # Add the original_tag to the topic
        topic.tags.add(original_tag)

        # Create a different tag
        different_tag = create_tag(user=self.user, name='Different Tag')
        # Create a payload with the existing tag name
        # to change the topic's tag to the different tag
        payload = {'tags': [{'name': 'Different Tag'}]}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Update the topic details with the different tag from the payload
        result = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the topic has one tag
        self.assertEqual(topic.tags.count(), 1)
        # Check that the topic has the different tag
        self.assertIn(different_tag, topic.tags.all())
        # Check that the topic does not have the original tag
        # because it has been replaced by the different tag
        self.assertNotIn(original_tag, topic.tags.all())

    def test_clear_topic_tags(self):
        """
        Test clearing a topic's tags.
        """

        # Create a topic
        topic = create_topic(user=self.user)
        # Create a tag
        tag = create_tag(user=self.user)
        # Add the tag to the topic
        topic.tags.add(tag)

        # Create a payload with no tags
        payload = {'tags': []}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Update the topic details with the payload
        result = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the topic has no tags
        self.assertEqual(topic.tags.count(), 0)
