"""Simple Unitesting for the Language model."""
from django.test import TestCase
from ..models import Multimedia
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('wipecardetailing')


class MultimediaModelTestClass(TestCase):
    """Test the Multimedia model"""

    @classmethod
    def setUpClass(cls):
        """Run at the start of the test of this class."""
        logger.debug("setUpClass started")
        cls.user = User.objects.get(id=2)
        logger.debug('cls user created: %s' % cls.user)

    def test_get_multimedia_title_link(self):
        """get the 1st multimedia object"""

        multimedia = Multimedia.objects.get(pk=1)
        logger.debug("multimedia: %s" % multimedia)
        logger.debug("multimedia title: %s" % multimedia.title)

        self.assertEquals(multimedia.title, 'First Car Wash')


    def test_create_multimedia_required_fields_only(self):
        """
        test the creation of the multimedia object with all
        required fields only.
        """
        multimedia = Multimedia.objects.create(
            title='a new car',
            type='SocialMediaLink',
            addedbyuser=self.user.pk,
            socialmedialink='http://fedal.nl'
        )
        multimedia.save()

        logger.debug("multimedia object created %s" % multimedia)
        logger.debug("multimedia title: %s" % multimedia.title)

        self.assertIsInstance(multimedia, Multimedia)


    # TODO: fix the url validation test because it should return an error
    def test_create_multimedia_invalid_url_error(self):
        """
        test the creation of the multimedia object with an invalid link url.
        expect an error
        """
        multimedia = Multimedia.objects.create(
            title='a new car with error',
            type='SocialMediaLink',
            addedbyuser=self.user.pk,
            socialmedialink='testlink_invalid'
        )
        multimedia.save()

        logger.debug("multimedia 2 object created %s" % multimedia)
        logger.debug("multimedia 2 link: %s" % multimedia.socialmedialink)

        self.assertIsInstance(multimedia, Multimedia)

    def test_applabel_multimedia(self):
        """expect the applabel to be wipecardetailing."""

        multimedia = Multimedia.objects.get(pk=1)
        applabel = str(multimedia._meta.app_label)

        logger.debug('applabel: %s' % applabel)

        self.assertEquals(applabel, 'wipecardetailing')


    @classmethod
    def tearDownClass(cls):
        """Run after all tests are done."""
        logger.debug("tearDownClass started")
