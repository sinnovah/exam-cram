"""
Serializers for the topic API.
"""
from rest_framework import serializers

from core.models import Topic


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic object.
    """

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the topic model
        model = Topic
        # Fields to include in the topic API
        fields = ['id', 'title', 'notes', 'last_modified']
        # Make the id and last_modified fields read only
        read_only_fields = ['id', 'last_modified']
