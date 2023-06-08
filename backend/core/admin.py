"""
Admin customizations for the project.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

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

    fieldsets = (
        # Translators _: Custom title of the details section
        (_('Details'), {'fields': ('first_name', 'last_name', 'email',)}),
        # Translators _: Custom title of the permissions section
        (_('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        # Translators _: Custom title of the important dates section
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # Make last login date read only (uneditable)
    readonly_fields = ('last_login',)


# Register the user model with the custom admin class
admin.site.register(models.User, CustomUserAdmin)
