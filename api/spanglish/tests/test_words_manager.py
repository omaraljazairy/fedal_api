"""Unitesting for the Word manager's functions."""

from django.test import TestCase
from ..models import Word
from ..managers import WordsManager
import logging

LOGGER = logging.getLogger('spanglish')


class WordsManagerTestClass(TestCase):
    """Test the WordsManager class."""

    @classmethod
    def setUpClass(cls):
        """Run at the start of the test of this class."""
        LOGGER.debug("setUpClass started")

    def test_get_word_object_instance(self):
        """Call the get_all_words_by_language and expect to
        get back a Word object instance.
        """

        data = Word.words.get_all_words_by_language()

        records = []
        for d in data:
            records.append(d)

        self.assertIsInstance(records[0], Word)

    def test_get_all_words_by_iso1(self):
        """Provide the function with then 'en' value as pararm.

        expect to get back one record.
        """
        ios_param = 'en'
        data = Word.words.get_all_words_by_language(iso1=ios_param)

        records = []
        for d in data:
            records.append(d.word)

        LOGGER.debug("records: %s" % records)

        self.assertTrue(len(records) == 1)

    def test_get_all_words_by_iso1_default_value(self):
        """No parameter will be provided, expect to get the
        same result as providing the en parameter.
        """

        data = Word.words.get_all_words_by_language()
        records = []
        for d in data:
            records.append(d.word)

        LOGGER.debug("records: %s" % records)

        self.assertTrue(len(records) == 1)

    def test_get_all_words_by_iso1_from_manager(self):
        """using the manager's method
        directly, expect to get the same result as providing
        the en parameter.
        """
        manager = WordsManager()
        data = WordsManager.get_all_words_by_language(manager)
        records = []
        for d in data:
            records.append(d.word)

        self.assertTrue(len(records) == 1)
        self.assertTrue(WordsManager.__dict__['get_all_words_by_language'])


    @classmethod
    def tearDownClass(cls):
        """Run after all tests are done."""
        LOGGER.debug("tearDownClass started")
