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
        fields = ['id', 'title', 'last_modified']
        # Make the id and last_modified fields read only
        read_only_fields = ['id', 'last_modified']


class TopicDetailSerializer(TopicSerializer):
    """
    Topic detail with additional fields.
    Extends the Topic object.
    """

    class Meta(TopicSerializer.Meta):
        """
        Meta class allows for validation rules for the data.
        Extends the Meta class from TopicSerializer.
        """

        # Add additional fields to the topic detail method
        fields = TopicSerializer.Meta.fields + ['notes']
