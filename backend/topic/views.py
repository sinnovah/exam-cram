"""
Topic API views.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Topic
from topic import serializers


class TopicViewSet(viewsets.ModelViewSet):
    """
    Manage topics [GET, POST, PUT, PATCH, DELETE].
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
