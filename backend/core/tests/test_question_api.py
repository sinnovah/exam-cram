"""
Unit tests for the Question API.
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from topic.serializers import QuestionSerializer

from core.models import Question
from core.tests.helpers import (
    create_user,
    create_question,
    question_details_url
)


# Question list endpoint constant
QUESTIONS_URL = reverse('topic:question-list')


class PublicQuestionApiTests(TestCase):
    """Test the publicly available Question API."""

    def setUp(self):
        """Set up the public question API test suite."""

        # Create a public client
        self.client = APIClient()

    def test_authentication_required_for_questions(self):
        """
        Test that authentication is required for retrieving questions.
        """

        # Attempt to retrieve questions
        response = self.client.get(QUESTIONS_URL)

        # Test that the request was not successful
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Test that the not authenticated error code is returned
        self.assertEqual(
            response.data['detail'].code, 'not_authenticated'
        )


class PrivateQuestionApiTests(TestCase):
    """
    Test suite for the question API (private access).
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

    def test_list_questions_successful(self):
        """
        Test retrieving a list of questions for the user is successful.
        """

        # Create some questions for the user
        create_question(user=self.user)
        create_question(user=self.user, name='Test Question 2')

        # Retrieve the 2 created questions
        response = self.client.get(QUESTIONS_URL)
        # Get the questions from the database
        # Ordered by most recently created
        questions = Question.objects.all().order_by('id')
        # Serialize the questions from the database
        # Many=True because we are serializing a list
        serializer = QuestionSerializer(questions, many=True)

        # Test that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there are 2 questions in the response
        self.assertEqual(len(response.data), 2)
        # Test that the questions in the response match the database
        self.assertEqual(response.data, serializer.data)

    def test_list_questions_limited_to_user(self):
        """
        Test that questions list is limited to the authenticated user.
        """

        # Create another new user
        other_user = create_user(email='other@example.com')

        # Create a question for the authenticated user
        create_question(user=self.user)
        # Create a question for the other user
        create_question(user=other_user, name='Test Question 2')

        # Retrieve the question for the authenticated user
        response = self.client.get(QUESTIONS_URL)
        # Get the questions from the database
        questions = Question.objects.filter(user=self.user)
        # Serialize the questions from the database
        serializer = QuestionSerializer(questions, many=True)

        # Test that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that there is 1 question in the response
        # Because we only created 1 question for the authenticated user
        self.assertEqual(len(response.data), 1)
        # Test that the question in the response match the database
        self.assertEqual(response.data, serializer.data)

    def test_patch_question_success(self):
        """
        Test updating a question with PATCH is successful.
        """

        # Create a question for the user
        question = create_question(user=self.user)
        # Create a new question name
        payload = {'name': 'New Question Name'}
        # URL for the question details
        url = question_details_url(question.id)
        # Update the question with PATCH
        response = self.client.patch(url, payload)

        # Refresh the question from the database
        question.refresh_from_db()

        # Test that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test that the question was updated successfully
        self.assertEqual(question.name, payload['name'])
