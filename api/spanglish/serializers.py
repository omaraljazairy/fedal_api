"""Serialize the Spanglish models."""

from .models import Word, Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """Serialize the category object."""

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Category
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
