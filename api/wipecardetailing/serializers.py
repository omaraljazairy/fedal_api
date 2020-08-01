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
        # they extra kwargs will be returned in the view during the validation before the save.
        extra_kwargs = {
            'status': {
                'error_messages': {
                    'required': 'Status field is required'
                }
            },
            'email': {
                'error_messages': {
                    'required': 'Email field is required',
                    'invalid': 'Invalid email'
                }
            },
            'formname': {
                'error_messages': {
                    'required': 'Formname field is required'
                }
            }
        }



class MultimediaSerializer(serializers.ModelSerializer):
    """Serialize the Multimedia object."""

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Multimedia
        fields = '__all__'

