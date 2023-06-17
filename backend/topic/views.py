"""
Topic API views.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Topic, Tag, Resource, Question
from topic import serializers


# Extend the schema for the TopicViewSet
# https://drf-spectacular.readthedocs.io/en/latest/customization.html#extend-schema
# adds additional OpenAPI documentation to the viewset
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of Tag ids to filter'
            ),
            OpenApiParameter(
                'resources',
                OpenApiTypes.STR,
                description='Comma separated list of Resource ids to filter'
            ),
            OpenApiParameter(
                'questions',
                OpenApiTypes.STR,
                description='Comma separated list of Question ids to filter'
            )
        ]
    )
)
class TopicViewSet(viewsets.ModelViewSet):
    """
    Manage topics.
    """
    # Extends DRF's ModelViewSet.

    # Set DRF's serializer class to the custom topic detail serializer
    serializer_class = serializers.TopicDetailSerializer
    # Set the queryset to all the topic objects
    queryset = Topic.objects.all()
    # Set the authentication for the viewset to token authentication
    authentication_classes = [TokenAuthentication]
    # Must be authenticated to use the viewset
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, query_string):
        """
        Convert a list of string IDs to a list of integers.
        """

        # Split the query string by commas
        string_ids = query_string.split(',')
        # Return the list of string IDs converted to integers
        return [int(str_id) for str_id in string_ids]

    def get_queryset(self):
        """
        Retrieve only the topics for the authenticated user
        """

        # Get the tags query string
        tags = self.request.query_params.get('tags')
        # Get the resources query string
        resources = self.request.query_params.get('resources')
        # Get the questions query string
        questions = self.request.query_params.get('questions')

        # Get the queryset
        queryset = self.queryset

        # If the tags query string is provided
        if tags:
            # Convert the tags query string to a list of integers
            tag_ids = self._params_to_ints(tags)
            # Filter the queryset by the tag IDs
            queryset = queryset.filter(tags__id__in=tag_ids)

        # If the resources query string is provided
        if resources:
            # Convert the resources query string to a list of integers
            resource_ids = self._params_to_ints(resources)
            # Filter the queryset by the resource IDs
            queryset = queryset.filter(resources__id__in=resource_ids)

        # If the questions query string is provided
        if questions:
            # Convert the questions query string to a list of integers
            question_ids = self._params_to_ints(questions)
            # Filter the queryset by the question IDs
            queryset = queryset.filter(questions__id__in=question_ids)

        # Return the topics (with any filtering applied) for the authenticated
        # user, ordered by most recently created, distinct topics only
        return queryset.filter(
                user=self.request.user
            ).order_by('-id').distinct()

    def get_serializer_class(self):
        """
        Return the appropriate serializer class.
        https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
        """

        # Return the list serializer if the action is list
        if self.action == 'list':
            return serializers.TopicSerializer

        # Return the default serializer (TopicDetailSerializer)
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new topic.
        https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself:~:text=Save%20and%20deletion%20hooks%3A
        """

        # Set the user to the authenticated user
        serializer.save(user=self.request.user)


# Extend the schema for the BaseTopicAttrViewSet
# https://drf-spectacular.readthedocs.io/en/latest/customization.html#extend-schema
# adds additional OpenAPI documentation to the viewset
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to topics'
            )
        ]
    )
)
class BaseTopicAttrViewSet(
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    Base reusable ViewSet for topic attributes
    (Objects with relationships to topics).
    """
    # Extends DRF's GenericViewSet and mixins.

    # Set the authentication for the viewsets to token authentication
    authentication_classes = [TokenAuthentication]
    # Must be authenticated to use the viewsets
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        # Get the assigned_only query string
        # If assigned_only is 1, return only the assigned objects
        # If assigned_only is 0, return all the objects
        # bool converts 1 to True and 0 to False
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )

        # Get the queryset
        queryset = self.queryset

        # If assigned_only is True
        if assigned_only:
            # Filter the queryset by objects that are assigned to topics
            queryset = queryset.filter(topic__isnull=False)

        # Return the queryset filtered by the authenticated user
        # Distinct objects only
        return queryset.filter(
            user=self.request.user
        ).distinct()


class TagViewSet(BaseTopicAttrViewSet):
    """
    Manage tags.
    """
    # Extends BaseTopicAttrViewSet.

    # Set DRF's serializer class to the custom tag serializer
    serializer_class = serializers.TagSerializer
    # Set the queryset to all the tag objects
    queryset = Tag.objects.all().order_by('name')


class ResourceViewSet(BaseTopicAttrViewSet):
    """
    Manage resources.
    """
    # Extends BaseTopicAttrViewSet.

    # Set DRF's serializer class to the custom resource serializer
    serializer_class = serializers.ResourceSerializer
    # Set the queryset to all the resource objects
    queryset = Resource.objects.all().order_by('name')


class QuestionViewSet(BaseTopicAttrViewSet):
    """
    Manage questions.
    """
    # Extends BaseTopicAttrViewSet.

    # Set DRF's serializer class to the custom question serializer
    serializer_class = serializers.QuestionSerializer
    # Set the queryset to all the question objects
    queryset = Question.objects.all().order_by('id')
