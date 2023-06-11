"""
User API URL mappings.
"""
from django.urls import path

from user import views

# App name for the user API
app_name = 'user'

# Url patterns for the user API
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('manage/', views.ManageUserView.as_view(), name='manage')
]
