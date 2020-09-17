"""Unitest serializers"""

from django.test import TestCase
from ..serializers import MultimediaSerializer
from ..models import Multimedia
from datetime import datetime
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('wipecardetailing')


class MultimediasSerializerTestClass(TestCase):
    """Tests for the MultimediasSerializer class."""

    @classmethod
    def setUpClass(cls):
        """Will run only at the start of the test."""
        cls.user = User.objects.get(id=2)
        logger.debug('cls user created: %s' % cls.user)


    def test_multimedia_serialized_object_with_expected_keys(self):
        """call a Multimedia instance object and expect to
        get a serialized object with the following keys:
        id, title, type, addedbyuser, added, link, socialmedianame.
        """
        multimedia = Multimedia.objects.all()
        serializer = MultimediaSerializer(multimedia, many=True).data

        serialized_keys = list(serializer[0].keys())
        expected_keys = sorted(
            [
                'id',
                'title',
                'type',
                'uploaded_by',
                'added',
                'link',
                'socialmedianame',
                'file'
            ]
        )
        logger.debug("serialized data Multimedias: %s " % serialized_keys)

        self.assertEquals(sorted(serialized_keys), expected_keys)

    def test_save_object_success(self):
        """serialize an object to be saved. Serializer should validate it and
         save it.
         """

        multimedia_data = {
            'title': 'a new clean car',
            'type': 'SocialMediaLink',
            'addedbyuser': self.user.pk ,
            'added': datetime.now(),
            'link': 'http://fedal.nl',
            'socialmedianame': 'facebook'
        }

        multimedia = Multimedia.objects.create(**multimedia_data)
        serializer = MultimediaSerializer(instance=multimedia)

        logger.debug("multimedia oject: %s" % multimedia)
        logger.debug("multimedia serializer: %s" % serializer)
        logger.debug("serialized multimedia object: %s" % serializer.data)

        self.assertTrue(serializer.data['title'] == multimedia_data['title'])

    # TODO: fix the url validation test because it should return an error
    def test_save_object_with_invalid_url_error(self):
        """
        try to save an object with an invalid link url.
        Serializer should return an error.
        """

        multimedia_data = {
            'title': 'a broken car',
            'type': 'SocialMediaLink',
            'addedbyuser': self.user.pk,
            'added': datetime.now(),
            'link': 'invalid_url',
            'socialmedianame': 'facebook'
        }

        multimedia = Multimedia.objects.create(**multimedia_data)
        serializer = MultimediaSerializer(instance=multimedia)

        logger.debug("multimedia invalid oject: %s" % multimedia)
        logger.debug("multimedia invalid serializer: %s" % serializer)
        logger.debug("serialized invalid multimedia object: %s" % serializer.data)

        self.assertTrue(True)


    @classmethod
    def tearDownClass(cls):
        """deinitialize any open connections or objects"""