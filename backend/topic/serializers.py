"""
Serializers for the topic API.
"""
from rest_framework import serializers

from core.models import (
    Topic,
    Tag,
    Resource,
    Question
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


class ResourceSerializer(serializers.ModelSerializer):
    """
    Resource object.
    """

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the resource model
        model = Resource
        # Fields to include in the resource API
        fields = ['id', 'name', 'link']
        # Make the id field read only
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question object.
    """

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the question model
        model = Question
        # Fields to include in the question API
        fields = ['id', 'name', 'answer', 'wrong_answers']
        # Make the id field read only
        read_only_fields = ['id']


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic object.
    """

    # List of tags (many=True) they have a nested
    # relationship to topic they are optional
    tags = TagSerializer(many=True, required=False)

    # List of resources (many=True) they have a nested
    # relationship to topic they are optional
    resources = ResourceSerializer(many=True, required=False)

    # List of questions (many=True) they have a nested
    # relationship to topic they are optional
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        """Meta class allows for validation rules for the data"""

        # Associate the serializer with the topic model
        model = Topic
        # Fields to include in the topic API
        fields = ['id',
                  'title',
                  'last_modified',
                  'tags',
                  'resources',
                  'questions']
        # Make the id and last_modified fields read only
        read_only_fields = ['id', 'last_modified']

    def _get_or_create_tags(self, tags, topic):
        """
        Get or create the tags if they do not exist.
        """

        # Get the authenticated user
        auth_user = self.context['request'].user

        # Iterate over the tags
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

    def _get_or_create_resources(self, resources, topic):
        """
        Get or create the resources if they do not exist.
        """

        # Get the authenticated user
        auth_user = self.context['request'].user

        # Iterate over the resources
        for resource in resources:
            # Get or create the resource if it does not exist
            # I.e., if the resource exists with the name and user passed in
            # arguments, get it, else create it avoiding duplicate resources.
            # **resource param allows for adding additional resource fields
            # in the future
            resource_object, created = Resource.objects.get_or_create(
                user=auth_user,
                **resource
            )
            # Add the resource to the topic
            topic.resources.add(resource_object)

    def _get_or_create_questions(self, questions, topic):
        """
        Get or create the questions if they do not exist.
        """

        # Get the authenticated user
        auth_user = self.context['request'].user

        # Iterate over the questions
        for question in questions:
            # Get or create the question if it does not exist
            # I.e., if the question exists with the name and user passed in
            # arguments, get it, else create it avoiding duplicate questions.
            # **question param allows for adding additional question fields
            # in the future
            question_object, created = Question.objects.get_or_create(
                user=auth_user,
                **question
            )
            # Add the question to the topic
            topic.questions.add(question_object)

    def create(self, validated_data):
        """
        Override the create method to allow create for nested serializers.
        """

        # Remove the tags from the validated data
        # Assign them to a tags variable
        # If no tags are passed in, set the tags variable to an empty list
        tags = validated_data.pop('tags', [])
        # Remove the resources from the validated data
        # Assign them to a resources variable
        # If no resources are passed in,
        # set the resources variable to an empty list
        resources = validated_data.pop('resources', [])
        # Remove the questions from the validated data
        # Assign them to a questions variable
        # If no questions are passed in,
        # set the questions variable to an empty list
        questions = validated_data.pop('questions', [])
        # Create the topic without the additional attributes
        topic = Topic.objects.create(**validated_data)

        # Call the _get_or_create_tags method to get
        # existing tags or create the tags
        self._get_or_create_tags(tags, topic)
        # Call the _get_or_create_resources method to get
        # existing resources or create the resources
        self._get_or_create_resources(resources, topic)
        # Call the _get_or_create_questions method to get
        # existing questions or create the questions
        self._get_or_create_questions(questions, topic)

        # Return the topic
        return topic

    def update(self, instance, validated_data):
        """
        Override the update method to allow update for nested serializers.
        """

        # Remove the tags from the validated data
        # Assign them to a tags variable
        # If no tags are passed in, set the tags variable to None
        tags = validated_data.pop('tags', None)
        # Remove the resources from the validated data
        # Assign them to a resources variable
        # If no resources are passed in, set the resources variable to None
        resources = validated_data.pop('resources', None)

        # If tags were passed in
        if tags is not None:

            # Clear the existing tags
            instance.tags.clear()

            # Call the _get_or_create_tags method to get
            # existing tags or create the tags
            self._get_or_create_tags(tags, instance)

        # If resources were passed in
        if resources is not None:

            # Clear the existing resources
            instance.resources.clear()

            # Call the _get_or_create_resources method to get
            # existing resources or create the resources
            self._get_or_create_resources(resources, instance)

        # Update the topic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the topic instance
        instance.save()
        # Return the topic
        return instance


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
