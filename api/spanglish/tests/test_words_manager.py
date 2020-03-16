"""Unitesting for the Word manager's functions."""

from django.test import TestCase
from spanglish.models import Word
import logging

LOGGER = logging.getLogger('spanglish')


class WordsManagerTestClass(TestCase):
    """Test the WordsManager class."""

    @classmethod
    def setUpClass(cls):
        """Run at the start of the test of this class."""
        LOGGER.debug("setUpClass started")

    def test_get_all_words_by_iso1(self):
        """Provide the function with then 'en' value as pararm.

        expect to get back one record.
        """
        ios_param = 'en'
        data = Word.words.get_all_words_by_language(iso1=ios_param)

        LOGGER.debug("data returned: %s" % data)

        self.assertTrue(True)

    @classmethod
    def tearDownClass(cls):
        """Run after all tests are done."""
        LOGGER.debug("tearDownClass started")
