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

    def create(self, validated_data):
        """
        Override the create method to allow create for nested serializers.
        """

        # Remove the tags from the validated data
        # Assign them to a tags variable
        tags = validated_data.pop('tags', [])
        # Create the topic without tags
        topic = Topic.objects.create(**validated_data)
        # Get the authenticated user
        auth_user = self.context['request'].user

        # Iterate over the popped tags
        for tag in tags:
            # Get or create the tag if it does not exist
            # I.e., if the tag exists with the name and user passed in
            # arguments, get it, else create it avoiding duplicate tags.
            # **tag param allows for adding additional tag fields in the future
            tag_object, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag
            )
            # Add the tag to the topic
            topic.tags.add(tag_object)

        # Return the topic
        return topic


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
