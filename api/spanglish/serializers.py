"""Serialize the Spanglish models."""

from .models import Word
from rest_framework import serializers


class WordSerializer(serializers.ModelSerializer):
    """Serialize the word object data."""

    translation = serializers.ReadOnlyField()
    language = serializers.ReadOnlyField()
    category = serializers.ReadOnlyField()

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Word
        fields = ('word', 'translation', 'category', 'language')
