"""
Topic API views.
"""
from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Topic, Tag
from topic import serializers


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

    def get_queryset(self):
        """
        Retrieve only the topics for the authenticated user
        """

        # Return the topics for the authenticated user
        # Ordered by most recently created
        return self.queryset.filter(user=self.request.user).order_by('-id')

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


class BaseTopicAttrViewSet(
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

        # Return the queryset filtered by the authenticated user
        return self.queryset.filter(
            user=self.request.user
        ).order_by('name')  # Order alphabetically by name


class TagViewSet(BaseTopicAttrViewSet):
    """
    Manage tags.
    """
    # Extends BaseTopicAttrViewSet.

    # Set DRF's serializer class to the custom tag serializer
    serializer_class = serializers.TagSerializer
    # Set the queryset to all the tag objects
    queryset = Tag.objects.all()
