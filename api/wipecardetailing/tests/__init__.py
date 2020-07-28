"""Run before the tests to load the fixtures."""
from __future__ import print_function
from django.conf import settings
from django.core.management import call_command
import warnings
# from django.core.cache import cache

warnings.filterwarnings('ignore', category=RuntimeWarning)


def setUpModule():
    """Run before any test in the package runs."""
    print("setup module wipecardetailing is running")

    # cache.delete_pattern("*")
    wipecardetailing_fixtures = settings.FIXTURES['wipecardetailing']
    call_command('loaddata', wipecardetailing_fixtures, verbosity=1)


def tearDownModule():
    """Clear all the tests."""
    print("teardown module wipecardetailing is done")
