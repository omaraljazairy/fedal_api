"""Serialize the Spanglish models."""

from .models import Formsubmits, Multimedia
from rest_framework import serializers
import logging

logger = logging.getLogger('wipecardetailing')

class FormSubmitsSerializer(serializers.ModelSerializer):
    """Serialize the formsubmits object."""

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Formsubmits
        fields = '__all__'


class MultimediaSerializer(serializers.ModelSerializer):
    """Serialize the Multimedia object."""

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Multimedia
        fields = '__all__'

