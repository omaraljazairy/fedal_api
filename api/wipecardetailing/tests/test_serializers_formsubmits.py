"""Unitest serializers"""

from django.test import TestCase
from ..serializers import FormSubmitsSerializer
from ..models import Formsubmits
import logging

logger = logging.getLogger('wipecardetailing')


class FormsubmitsSerializerTestClass(TestCase):
    """Tests for the FormsubmitsSerializer class."""

    @classmethod
    def setUpClass(cls):
        """Will run only at the start of the test."""

    def test_Formsubmits_serialized_object_with_expected_keys(self):
        """call a Formsubmits instance object and expect to
        get a serialized object with the following keys:
        id, name, iso1, added.
        """
        submits = Formsubmits.objects.all()
        serializer = FormSubmitsSerializer(submits, many=True).data

        serialized_keys = list(serializer[0].keys())
        expected_keys = sorted(
            [
                'id',
                'formname',
                'companyname',
                'customername',
                'email',
                'phonenumber',
                'streetname',
                'housenumber',
                'postcode',
                'city',
                'message',
                'submitted',
                'status'
            ]
        )
        logger.debug("serialized data Formsubmits: %s " % serialized_keys)

        self.assertEquals(sorted(serialized_keys), expected_keys)


    @classmethod
    def tearDownClass(cls):
        """deinitialize any open connections or objects"""