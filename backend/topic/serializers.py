"""
Serializers for the topic API.
"""
from rest_framework import serializers

from core.models import (
    Topic,
    Tag
)


class TagSerializer(serializers.ModelSerializer):
    """
    Tag object.
    """

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the tag model
        model = Tag
        # Fields to include in the tag API
        fields = ['id', 'name']
        # Make the id field read only
        read_only_fields = ['id']


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic object.
    """

    # List of tags (many=True) have a nested
    # relationship to topic they are optional
    tags = TagSerializer(many=True, required=False)

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the topic model
        model = Topic
        # Fields to include in the topic API
        fields = ['id', 'title', 'last_modified', 'tags']
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
