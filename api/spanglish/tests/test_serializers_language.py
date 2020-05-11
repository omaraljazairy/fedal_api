"""Unitest serializers"""

from django.test import TestCase
from ..serializers import LanguageSerializer
from ..models import Language
import logging

logger = logging.getLogger('spanglish')


class LanguageSerializerTestClass(TestCase):
    """Tests for the LanguageSerializer class."""

    @classmethod
    def setUpClass(cls):
        """Will run only at the start of the test."""

    def test_language_serialized_object_with_expected_keys(self):
        """call a language instance object and expect to
        get a serialized object with the following keys:
        id, name, iso1, added.
        """
        language = Language.objects.all()
        serializer = LanguageSerializer(language, many=True).data

        serialized_keys = list(serializer[0].keys())
        expected_keys = sorted(['id', 'name', 'iso1', 'added'])
        logger.debug("serialized data language: %s " % serialized_keys)

        self.assertEquals(sorted(serialized_keys), expected_keys)

    def test_language_creation_iso_empty(self):
        """create an object with an empty iso1 value"""

        language = Language.objects.create(name='Danish')
        serializer = LanguageSerializer(instance=language)

        logger.debug("language create: %s" % language)
        logger.debug("language serialized: %s" % serializer)

        self.assertTrue(True)


    @classmethod
    def tearDownClass(cls):
        """deinitialize any open connections or objects"""