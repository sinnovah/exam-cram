"""
Unit tests for creating and assigning questions to topics.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests.helpers import (
    create_user,
    create_question,
)
from core.models import Topic


# Topic list endpoint constant
TOPICS_URL = reverse('topic:topic-list')


class PrivateTopicQuestionsApiTests(TestCase):
    """
    Test suite for the topic questions (private access).
    Authenticated requests.
    """

    def setup(self):
        """Set up the test suite."""

        # Create a test client to make test http requests
        self.client = APIClient()
        # Create a test user
        self.user = create_user()

        # Authenticate the test user
        self.client.force_authenticate(user=self.user)

        # Topic data to send to endpoints
        self.payload = {
            'title': 'Payload Topic',
            'notes': 'Payload notes for my topic',
            'questions': [
                {
                    'name': 'Payload Question',
                    'answer': 'Payload Answer',
                    'wrong_answers': ['Payload Wrong Answer',
                                      'Payload Second Wrong Answer']
                },
                {
                    'name': 'Payload Question 2',
                    'answer': 'Payload Answer 2',
                    'wrong_answers': ['Payload Wrong Answer 2',
                                      'Payload Second Wrong Answer 2']
                }
            ]
        }

    def test_create_topic_with_existing_questions_successful(self):
        """
        Test creating a topic with existing
        question does not duplicate the question.
        """

        # Create an existing question
        existing_question = create_question(
            user=self.user,
            name='Payload Question'
        )
        # Post the payload with the same question name as the existing question
        response = self.client.post(TOPICS_URL, self.payload, format='json')

        # Test that the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the user's topics from the database
        topics = Topic.objects.filter(user=self.user)

        # Check that there is one topic
        self.assertEqual(topics.count(), 1)

        # Get the first and only topic from the queryset
        topic = topics[0]

        # Check that the topic has two questions
        self.assertEqual(topic.questions.count(), 2)

        # Check that the existing question is in the topic
        # (not duplicated)
        self.assertIn(existing_question, topic.questions.all())

        # Iterate through the topic's questions
        for questions in self.payload['questions']:
            # Check that the user's questions
            # exist ans match the payload
            self.assertTrue(
                topic.questions.filter(
                    user=self.user,
                    name=questions['name'],
                    answer=questions['answer'],
                    wrong_answers=questions['wrong_answers']
                ).exists()
            )
