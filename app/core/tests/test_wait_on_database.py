"""
Unit tests for custom management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OperationalError

from django.core.management import call_command
from django.db.utils import OperationalError as DjangoOperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_on_database.Command.check')
class ManagementCommandsTest(SimpleTestCase):
    """
    Test suite for custom management commands.
    Patched check to simulate exceptions in the response.
    """

    def test_wait_on_database_database_available(self, patch_check):
        """Test wait_on_database command when the database is available."""

        # Patched check method returns a True value
        patch_check.return_value = True

        # Call the command being tested
        call_command('wait_on_database')

        # Test patched check was called once
        self.assertEqual(patch_check.call_count, 1)
        # Test patched check was called with the correct parameters
        patch_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')  # Patch time.sleep to speed up test
    def test_wait_on_database_django_errors(self, patch_sleep, patch_check):
        """Test wait_on_database command when Django errors returned."""

        # Patched check returns a True value after six Django errors
        patch_check.side_effect = [DjangoOperationalError] * 6 + [True]

        # Call the command being tested
        call_command('wait_on_database')

        # Test that patched check was called seven times
        self.assertEqual(patch_check.call_count, 7)
        # Test patched check was called with the correct parameters
        patch_check.assert_called_with(databases=['default'])

    @patch('time.sleep')  # Patch time.sleep to speed up test
    def test_wait_on_database_psycopg2_errors(self, patch_sleep, patch_check):
        """Test wait_on_database command when Psycopg2 errors returned."""

        # Patched check returns a True value after four Psycopg2 errors
        patch_check.side_effect = [Psycopg2OperationalError] * 4 + [True]

        # Call the command being tested
        call_command('wait_on_database')

        # Test that patched check was called five times
        self.assertEqual(patch_check.call_count, 5)
        # Test patched check was called with the correct parameters
        patch_check.assert_called_with(databases=['default'])

    @patch('time.sleep')  # Patch time.sleep to speed up test
    def test_wait_on_database_mixed_errors(self, patch_sleep, patch_check):
        """Test wait_on_database command when mixed errors returned."""

        # Patched check returns a True value after five mixed errors
        patch_check.side_effect = [Psycopg2OperationalError] * 2 + \
            [DjangoOperationalError] * 3 + [True]

        # Call the command being tested
        call_command('wait_on_database')

        # Test that patched check was called six times
        self.assertEqual(patch_check.call_count, 6)
        # Test patched check was called with the correct parameters
        patch_check.assert_called_with(databases=['default'])
