"""
Django command to pause execution until database is available.
"""
import time

from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2OperationalError
from django.db.utils import OperationalError as DjangoOperationalError


class Command (BaseCommand):
    """
    Django command to pause execution until database is available.
    Extends BaseCommand class from django.core.management.base.
    """

    def handle(self, *args, **options):
        """Handle command stub, custom code follows"""

        # Initialise database up to false
        database_up = False

        # Print an appropriate message to terminal
        self.stdout.write('\nChecking database...')

        # While database is not up
        while not database_up:
            # Try to check database
            try:
                self.check(databases=['default'])
                database_up = True  # Database is up, set to true
            # If OperationalError exception is raised
            except (Psycopg2OperationalError, DjangoOperationalError):
                # Print an appropriate message to terminal
                self.stdout.write('Database unavailable, waiting 1 second...')
                # Wait one second
                time.sleep(1)

        # Print an appropriate success message to terminal (coloured green)
        self.stdout.write(self.style.SUCCESS('Database available!'))
