"""
Unit tests for models.
"""
from django.test import TestCase

from core.tests.helpers import (
    create_user,
    create_superuser,
    create_topic,
    create_tag
)

# Default values of create_user and create_superuser helper functions
USER = 'user@example.com'
SUPERUSER = 'superuser@example.com'
PASSWORD = 'ThirtyHairyHippos896'

# Default values of create_topic helper function
TOPIC_TITLE = 'Test Topic'
TOPIC_NOTES = 'Test notes for my topic'

# Default value of create_tag helper function
TAG_NAME = 'Test Tag'


class ModelTests(TestCase):
    """Test suite for the models in the project."""

    def test_create_user_with_email_success(self):
        """Test creating a new user with an email is successful."""

        # Create the user
        user = create_user()

        # Test that the user's email was created successfully
        self.assertEqual(user.email, USER)
        # Test that the user's password was created successfully
        # check_password checks the hashed password
        self.assertTrue(user.check_password, PASSWORD)

    def test_user_email_normalized(self):
        '''
        Test that emails for new users are normalized
        '''

        # List of input emails and expected normalized output emails
        # As per email spec:
        # Everything before the @ symbol should retain case
        # Everything after the @ symbol should be lowercase
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        # Loop through the sample emails
        for input_email, output_email in sample_emails:
            # Create the user
            user = create_user(email=input_email)
            # Test that the user's email was normalized successfully
            self.assertEqual(user.email, output_email)

    def test_create_user_with_empty_email_error(self):
        '''Test that creating a user without an email raises a ValueError'''

        # Test that a ValueError exception is raised
        with self.assertRaises(ValueError):
            # Create the user with an empty, invalid email
            create_user(email='')

    def test_create_superuser(self):
        '''Test creating a new superuser'''

        # Create the superuser
        superuser = create_superuser()

        # Check that the user is a superuser and staff
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_topic_success(self):
        """Test creating a new topic is successful."""

        # Create a user
        user = create_user()

        # Create the topic for the user
        topic = create_topic(user=user)

        # Test that the topic's title, notes user
        # and user were created successfully
        self.assertEqual(topic.title, TOPIC_TITLE)
        self.assertEqual(topic.notes, TOPIC_NOTES)
        self.assertEqual(topic.user, user)
        # Test that the string representation of the topic is the title
        self.assertEqual(str(topic), topic.title)
        # Test that the last_modified DataTime field is not None
        self.assertIsNotNone(topic.last_modified)

    def test_create_tag_success(self):
        """Test creating a new tag is successful."""

        # Create a user
        user = create_user()
        # Create the tag instance
        tag = create_tag(user=user)

        # Test that the tag's name and user were created successfully
        self.assertEqual(tag.name, TAG_NAME)
        self.assertEqual(tag.user, user)
        # Test that the string representation of the tag is the name
        self.assertEqual(str(tag), tag.name)
