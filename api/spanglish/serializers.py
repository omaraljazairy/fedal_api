"""Serialize the Spanglish models."""

from .models import Word, Category, Language
from rest_framework import serializers
import logging

logger = logging.getLogger('spanglish')


class CategorySerializer(serializers.ModelSerializer):
    """Serialize the category object."""

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Category
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    """Serialized the Language object."""

    iso1 = serializers.CharField(allow_blank=False, required=True, allow_null=True)

    def validate_empty_values(self, data):
        logger.debug("language serialized data validation %s" % data)
        return False

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Language
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    """Serialize the word object data."""

    translation = serializers.ReadOnlyField()
    language = serializers.ReadOnlyField()
    category = serializers.ReadOnlyField()

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Word
        fields = ('word', 'translation', 'category', 'language')
