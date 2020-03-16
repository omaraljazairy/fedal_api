"""using the different database object in the settings.

So the Spanglish app uses a different database / server
than other apps.
"""

import logging

LOGGER = logging.getLogger('spanglish')
APP_LABEL = 'spanglish'
DB = 'spanglish'


class DBRouter(object):
    """A router to control Q and Devops db operations."""

    def db_for_read(self, model, **hints):
        """Attempt to read auth models go to auth_db."""
        if model._meta.app_label == APP_LABEL:
            return DB
        return None

    def db_for_write(self, model, **hints):
        """Attempt to write spanglish models go to Spanglish db."""
        if model._meta.app_label == APP_LABEL:
            return None
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the spanglish app is involved."""
        if obj1._meta.app_label == APP_LABEL or \
           obj2._meta.app_label == APP_LABEL:
            return True
        return None
