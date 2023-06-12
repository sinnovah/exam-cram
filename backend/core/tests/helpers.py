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
    '''
    Helper function to create users for testing.
    '''

    # Create the user
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name)


def create_superuser(
        email='superuser@example.com',
        password='ThirtyHairyHippos896',):
    '''
    Helper function to create superusers for testing.
    '''

    # Create the superuser
    return get_user_model().objects.create_superuser(
        email=email,
        password=password,
    )


def create_topic(
        title='Test Topic',
        notes='Test notes for my topic',
        **params):  # Allows for additional parameters to be passed in
    '''
    Helper function to create topics for testing.
    '''

    # Create the topic for the user
    return models.Topic.objects.create(
        title=title,
        notes=notes,
        **params
    )


def topic_details_url(topic_id):
    '''
    Helper function returns topic detail urls for testing.
    '''

    # Return the url for the topic detail
    return reverse('topic:topic-detail', args=[topic_id])


def create_tag(
        name='Test Tag',
        **params):  # Allows for additional parameters to be passed in
    '''
    Helper function to create tags for testing.
    '''

    # Create the tag for the user
    return models.Tag.objects.create(
        name=name,
        **params
    )
