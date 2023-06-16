"""
Helpers to reuse in tests.
"""
# Use get_user_model to access the custom user model
# Allows for a change to the default user model
from django.contrib.auth import get_user_model
from django.urls import reverse

from core import models


def create_user(
        email='user@example.com',
        password='ThirtyHairyHippos896',
        first_name='Test',
        last_name='User'):
    """
    Helper function to create users for testing.
    """

    # Create the user
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name)


def create_superuser(
        email='superuser@example.com',
        password='ThirtyHairyHippos896',):
    """
    Helper function to create superusers for testing.
    """

    # Create the superuser
    return get_user_model().objects.create_superuser(
        email=email,
        password=password,
    )


def create_topic(
        title='Test Topic',
        notes='Test notes for my topic',
        **params):  # Allows for additional parameters to be passed in
    """
    Helper function to create topics for testing.
    """

    # Create the topic for the user
    return models.Topic.objects.create(
        title=title,
        notes=notes,
        **params
    )


def create_tag(user, name='Test Tag'):
    """
    Helper function to create tags for testing.
    """

    # Create the tag for the user
    return models.Tag.objects.create(
        user=user,
        name=name
    )


def create_resource(user, name='Test Resource', link='https://example.com'):
    """
    Helper function to create resources for testing.
    """

    # Create the resource for the user
    return models.Resource.objects.create(
        user=user,
        name=name,
        link=link
    )


def create_question(
        user,
        name='Test Question',
        answer='Test Answer',
        wrong_answers=['Test Wrong Answer 1', 'Test Wrong Answer 2'],
        **params):  # Allows for additional parameters to be passed in
    """
    Helper function to create resources for testing.
    """

    # Create the question for the user
    return models.Question.objects.create(
        user=user,
        name=name,
        answer=answer,
        wrong_answers=wrong_answers,
        **params
    )


def topic_details_url(topic_id):
    '''
    Helper function returns topic detail urls for testing.
    '''

    # Return the url for the topic detail
    return reverse('topic:topic-detail', args=[topic_id])


def tag_details_url(tag_id):
    '''
    Helper function returns tag detail urls for testing.
    '''

    # Return the url for the topic detail
    return reverse('topic:tag-detail', args=[tag_id])


def resource_details_url(resource_id):
    '''
    Helper function returns resource detail urls for testing.
    '''

    # Return the url for the topic detail
    return reverse('topic:resource-detail', args=[resource_id])


def question_details_url(question_id):
    '''
    Helper function returns question detail urls for testing.
    '''

    # Return the url for the topic detail
    return reverse('topic:question-detail', args=[question_id])
