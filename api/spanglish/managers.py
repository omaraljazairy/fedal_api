"""A seperate module for the managers.

I'm going to us sql raw throughout this project
Which will make me mix the models in two or three
managers.
"""

from django.db import models
import pytz
import logging
from django.conf import settings

LOGGER = logging.getLogger("spanglish")
otz = pytz.timezone('Europe/Amsterdam')


class WordsQuerySet(models.QuerySet):
    """create functions that will interact with the Word object."""

    def fetch_words(self, iso1):
        """Return QueryRaw result.

        Take the language iso1 as argument and returns all the related words.
        """
        params = [iso1]
        sql = "select w.Id, Word as 'word', c.Name as 'category', \
        Translation as 'translation', l.Name as 'language' \
        from " + settings.DATABASE_RAW_TABLES['word'] + "\
        as w join " + settings.DATABASE_RAW_TABLES['category'] + "\
        as c on (CategoryId = c.Id) \
        join " + settings.DATABASE_RAW_TABLES['translation'] + " as t \
        on (WordId = w.Id) \
        join " + settings.DATABASE_RAW_TABLES['language'] + "\
        as l on (LanguageId = l.Id) where ISO1 = %s;"

        # LOGGER.debug("fetch word called with iso1: %s" % iso1)
        # LOGGER.debug("fetch word called with sql: %s" % sql)

        translations = {
            'word': 'word',
            'category': 'category',
            'translation': 'translation',
            'language': 'language',
        }
        from .models import Word
        result = Word.words.raw(sql, params, translations)

        # LOGGER.debug("result returned: %s" % result)

        return result


class WordsManager(models.Manager):
    """A managers for the Word model.

    it will be the interface for the model queries.
    """

    def get_queryset(self):
        """Return the WordsQuerySet object."""
        return WordsQuerySet(self.model, using=self._db)

    def get_all_words_by_language(self, iso1='en'):
        """Return the fetch_word QuerySet object.

        takes the iso1 as a parameter, in this case the default value is en
        """
        data = self.get_queryset().fetch_words(iso1=iso1)
        # LOGGER.debug("data returned %s" % data)

        return data
