"""
Unit tests for the topic API.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import (
    create_user,
    create_topic,
    create_topic_url
)
from core.models import Topic

from topic.serializers import (
    TopicSerializer,
    TopicDetailSerializer
)

# Topic API URL endpoint constants
TOPICS_URL = reverse('topic:topic-list')


class PublicTopicApiTests(TestCase):
    """
    Test suite for the topic API (public access).
    Unauthenticated requests.
    """

    def setUp(self):
        """Set up the test suite."""

        # Create a test client to make test http requests
        self.client = APIClient()

    def test_authentication_required_for_topics(self):
        """
        Test that authentication is required for retrieving topics.
        """

        # Attempt to retrieve topics without authentication
        response = self.client.get(TOPICS_URL)

        # Assert that the request was not successful
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Test that the not authenticated error code is returned
        self.assertEqual(
            response.data['detail'].code, 'not_authenticated'
        )


class PrivateTopicApiTests(TestCase):
    """
    Test suite for the topic API (private access).
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
        }

    def test_list_topics_success(self):
        """
        Test retrieving and listing topics for a user is successful.
        """

        # Create a test topic for the user
        create_topic(user=self.user)
        # Create a second test topic for the user
        create_topic(user=self.user)

        # Retrieve the two created topics
        response = self.client.get(TOPICS_URL)
        # Retrieve all topics from the database
        # Ordered by most recently created
        topics = Topic.objects.all().order_by('-id')
        # Serialize the topics retrieved from the database
        # Many=True because we are serializing a list of topic objects
        serializer = TopicSerializer(topics, many=True)

        # Test that the get topics request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there are 2 topics in the response
        self.assertEqual(len(response.data), 2)
        # Test that the topics in the response match
        # the serialized topics from the database
        self.assertEqual(response.data, serializer.data)

    def test_list_topics_limited_to_user(self):
        """
        Test that the topics list is limited to the authenticated user.
        """

        # Create another test user
        other_user = create_user(email='other@example.com')

        # Create a test topic for the other user
        create_topic(user=other_user)
        # Create a test topic for the authenticated user
        create_topic(user=self.user)

        # Retrieve the topic for the authenticated user
        response = self.client.get(TOPICS_URL)
        # Retrieve topics from the database
        topics = Topic.objects.filter(user=self.user)
        # Serialize the topics retrieved from the database
        # Many=True because we are serializing a list of topic objects
        serializer = TopicSerializer(topics, many=True)

        # Test that the get topics request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there is 1 topic in the response
        self.assertEqual(len(response.data), 1)
        # Test that the topics in the response match
        # the serialized topics from the database
        self.assertEqual(response.data, serializer.data)

    def test_get_topic_detail_success(self):
        """
        Test retrieving a singular topic detail is successful.
        """

        # Create a test topic for the user
        topic = create_topic(user=self.user)
        # URL for the topic, passing in the topic id
        url = create_topic_url(topic.id)
        # Retrieve the topic for the authenticated user
        response = self.client.get(url)
        # Serialize the topic retrieved from the database
        serializer = TopicDetailSerializer(topic)

        # Test that the get topic request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that the topic in the response matches
        # the serialized topic from the database
        self.assertEqual(response.data, serializer.data)

    def test_create_topic_success(self):
        """
        Test creating a topic is successful.
        """

        # Create a topic for the user
        response = self.client.post(TOPICS_URL, self.payload)

        # Test that the create topic post request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve the topic from the database by response's id
        topic = Topic.objects.get(id=response.data['id'])

        # Iterate over the payload
        for key, value in self.payload.items():
            # Test that the payload's value matches the topics's value
            # getattr() to get the topic values with the payload's keys
            self.assertEqual(value, getattr(topic, key))

        # Test that the topic's user is the authenticated user
        self.assertEqual(topic.user, self.user)
