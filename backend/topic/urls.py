"""
Topic API URL mappings.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from topic import views

# Create a router for the topic API
router = DefaultRouter()
# Register the viewsets with the router. Automatically
# assigns GET, POST, PUT, PATCH, and DELETE methods
router.register('topics', views.TopicViewSet)
router.register('tags', views.TagViewSet)
router.register('resources', views.ResourceViewSet)
router.register('questions', views.QuestionViewSet)

# App name for the topic API
app_name = 'topic'

# Url patterns for the topic API
urlpatterns = [
    # Include the auto router urls in the urlpatterns
    path('', include(router.urls))
]
