"""
Admin customizations for the project.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core import models


class CustomUserAdmin(UserAdmin):
    """
    Custom admin pages for users.
    Extends Django's default UserAdmin.
    """

    # Order users by id
    ordering = ['id']
    # Display email and names on user list
    list_display = ['first_name', 'last_name', 'email']


# Register the user model with the custom admin class
admin.site.register(models.User, CustomUserAdmin)
