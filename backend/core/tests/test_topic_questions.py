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
    create_topic,
    topic_details_url
)
from core.models import Topic, Question


# Topic list endpoint constant
TOPICS_URL = reverse('topic:topic-list')


class PrivateTopicQuestionsApiTests(TestCase):
    """
    Test suite for the topic questions (private access).
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
            name='Payload Question',
            answer='Payload Answer',
            wrong_answers=[
                'Payload Wrong Answer',
                'Payload Second Wrong Answer']
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

    def test_create_question_on_topic_patch(self):
        """
        Test creating a new question when patching a topic.
        """

        # Create a topic
        topic = create_topic(user=self.user)
        # Create a payload with a different question name
        payload = {'questions': [{'name': 'Different Question'}]}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Patch the topic with the payload
        response = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the topic has one question
        self.assertEqual(topic.questions.count(), 1)

        # Get the new question from the database
        new_question = Question.objects.get(name='Different Question')

        # Check that the new question is in the topic
        self.assertIn(new_question, topic.questions.all())

    def test_patch_topic_by_assigning_existing_question(self):
        """
        Test patching a topic by assigning an existing question.
        """

        # Create an original question
        original_question = create_question(user=self.user)
        # Create a topic
        topic = create_topic(user=self.user)

        # Add the original question to the topic
        topic.questions.add(original_question)

        # Create a different question
        different_question = create_question(
            user=self.user, name='Different Question'
        )
        # Create a payload with the different question's name
        # to change the topic's question to the different question
        payload = {'questions': [{
            'name': 'Different Question',
            'answer': 'Test Answer',
            'wrong_answers': [
                'Test Wrong Answer 1',
                'Test Wrong Answer 2'
                ]
        }]}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Patch the topic with the payload
        response = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the topic has one question
        self.assertEqual(topic.questions.count(), 1)
        # Check that the different question is in the topic
        self.assertIn(different_question, topic.questions.all())
        # Check that the original question is not in the topic
        # because it has been replaced by the different question
        self.assertNotIn(original_question, topic.questions.all())

    def test_clear_topic_questions(self):
        """
        Test clearing a topic's questions.
        """

        # Create a topic
        topic = create_topic(user=self.user)
        # Create a question
        question = create_question(user=self.user)
        # Add the question to the topic
        topic.questions.add(question)

        # Create a payload with an empty list of questions
        payload = {'questions': []}
        # Get the topic details url
        url = topic_details_url(topic.id)
        # Patch the topic with the payload
        response = self.client.patch(url, payload, format='json')

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the topic has no questions
        self.assertEqual(topic.questions.count(), 0)
