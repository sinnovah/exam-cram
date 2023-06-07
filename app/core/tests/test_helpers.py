"""
Helpers to reuse in tests.
"""
# Use get_user_model to access the custom user model
# Allows for a change to the default user model
from django.contrib.auth import get_user_model


def create_user(email='user@example.com', password='testpass123'):
    '''
    Helper function to create user(s). If creating more than one user
    in the same test, pass in unique_ids for emails to avoid duplicate.
    '''

    # Create the user
    return get_user_model().objects.create_user(email, password)
