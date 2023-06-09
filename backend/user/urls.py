"""
User API URL mappings.
"""
from django.urls import path

from user import views

# App name to add 'user/' in the URL path
app_name = 'user'

# Url patterns after the app name
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name = 'create')
]