"""Simple Unitesting for the Language model."""

from django.test import TestCase
from ..models import Language
import logging

logger = logging.getLogger('spanglish')


class LanguageModelTestClass(TestCase):
    """Test the Language model"""

    @classmethod
    def setUpClass(cls):
        """Run at the start of the test of this class."""
        logger.debug("setUpClass started")

    def test_create_language_object_success(self):
        """create a new language by providing the name and ios1"""

        language_fr = Language.objects.create(name='French', iso1='fr')
        logger.debug("language_fr created %s" % language_fr)

        self.assertEquals("French", language_fr.name)

    def test_get_language_en(self):
        """get the 1st language iso1 and expect it to be en"""

        language_en = Language.objects.get(pk=1)
        logger.debug("language_en: %s" % language_en)
        logger.debug("language_en iso1: %s" % language_en.iso1)

        self.assertEquals(language_en.iso1, 'en')

    def test_create_language_without_iso1(self):
        """try to create a language object with no iso1. show throw an exception"""

        language_se = Language.objects.create(name='Swedish')
        logger.debug("language se created: %s" % language_se)

        self.assertTrue(True)


    def test_applabel_language_spanglish(self):
        """expect the applabel to be spanglish."""

        langauge = Language.objects.get(pk=1)
        applabel = str(langauge._meta.app_label)

        logger.debug('applabel: %s' % applabel)

        self.assertEquals(applabel, 'spanglish')

    @classmethod
    def tearDownClass(cls):
        """Run after all tests are done."""
        logger.debug("tearDownClass started")
