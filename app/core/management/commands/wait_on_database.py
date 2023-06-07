"""
Django command to pause execution until database is available.
"""
from django.core.management.base import BaseCommand


class Command (BaseCommand):
    """
    Django command to pause execution until database is available.
    Extends BaseCommand class from django.core.management.base.
    """

    def handle(self, *args, **options):
        """Handle command stub, custom code follows"""

        # Pass for now, will be implemented later
        pass
