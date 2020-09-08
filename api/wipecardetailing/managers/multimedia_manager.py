"""A seperate module for the managers.

I'm going to use sql raw throughout this model
Which will make me mix the models in two or three
managers.
"""

from django.db import models
import pytz
import logging
from django.conf import settings

logger = logging.getLogger(settings.AWS_LOGGER_NAME)
otz = pytz.timezone('Europe/Amsterdam')


class MultimediaQuerySet(models.QuerySet):
    """create functions that will interact with the Multimedia object."""

    def fetch(self, **kwargs):
        """Return QueryRaw result.

        Take the language iso1 as argument and returns all the related words.
        """
        params = kwargs.keys() # convert the params keys to a list
        values = kwargs.values() # conver the values to a list
        # create a string for the where clause that loops through the params list
        # and appends a " = %s " in front of every key.
        where_clause = ' = %s and '.join(params).__add__(' = %s') if len(params) else ' 1'
        sql = "select Id, Title, Type, Added, Link, SocialMediaName \
        from " + settings.DATABASE_RAW_TABLES['multimedia'] + " where " + where_clause

        logger.debug("manager kwargs: %s" % kwargs )
        logger.debug("manager params: %s" % params)
        logger.debug("manager values: %s" % values)
        logger.debug("manager where_clause: %s" % where_clause)
        logger.debug("manager sql: %s" % sql)

        result = self.raw(sql, values)

        logger.debug("result returned: %s" % result)

        return result


class MultimediaManager(models.Manager):
    """
    A managers for the Multimedia model.
    it will be the interface for the model queries.
    """

    def get_queryset(self):
        """Return the MultimediaQuerySet object."""
        return MultimediaQuerySet(self.model, using=self._db)

    def get_links(self, **kwargs):
        """Returns QuerySet object.
        takes the kwargs as a parameter.
        """
        data = self.get_queryset().fetch(**kwargs)
        # logger.debug("data returned %s" % data)

        return data
