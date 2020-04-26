"""Unitest serializers"""

from django.test import TestCase
from ..serializers import CategorySerializer
from ..models import Category
import logging

LOGGER = logging.getLogger('spanglish')


class CategorySerializerTestClass(TestCase):
    """Tests for the CategorySerializer class."""

    @classmethod
    def setUpClass(cls):
        """Will run only at the start of the test."""

    def test_get_serialized_object_with_expected_keys(self):
        """call a category instance object and expect to
        get a serialized object with the following keys:
        id, name, created.
        """
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True).data

        serialized_keys = list(serializer[0].keys())
        expected_keys = sorted(['id', 'name', 'created'])
        LOGGER.debug("serialized data category: %s " % serialized_keys)

        self.assertEquals(sorted(serialized_keys), expected_keys)

    @classmethod
    def tearDownClass(cls):
        """deinitialize any open connections or objects"""