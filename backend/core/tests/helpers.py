"""
Helpers to reuse in tests.
"""
# Use get_user_model to access the custom user model
# Allows for a change to the default user model
from django.contrib.auth import get_user_model


def create_user(email='user@example.com', password='ThirtyHairyHippos896'):
    '''
    Helper function to create users for testing.
    '''

    # Create the user
    return get_user_model().objects.create_user(email, password)

def create_superuser(email='superuser@example.com', password='ThirtyHairyHippos896'):
    '''
    Helper function to create superusers for testing.
    '''

    # Create the superuser
    return get_user_model().objects.create_superuser(email, password)
