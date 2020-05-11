"""Unitest serializers"""

from django.test import TestCase
from ..serializers import WordSerializer
from ..models import Word
import logging

logger = logging.getLogger('spanglish')


class WordSerializerTestClass(TestCase):
    """Tests for the WordSerializer class."""

    @classmethod
    def setUpClass(cls):
        """Will run only at the start of the test."""

    def test_get_serialized_object_with_expected_keys(self):
        """call the get_words_by_language and expect to
        get a serialized object with the following keys:
        word, category, translation, language
        """
        words = Word.words.get_all_words_by_language(iso1='en')
        serializer = WordSerializer(words, many=True).data

        serialized_keys = list(serializer[0].keys())
        expected_keys = sorted(['word', 'category', 'translation', 'language'])
        logger.debug("serialized data word: %s " % serialized_keys)

        self.assertEquals(sorted(serialized_keys), expected_keys)

    @classmethod
    def tearDownClass(cls):
        """deinitialize any open connections or objects"""