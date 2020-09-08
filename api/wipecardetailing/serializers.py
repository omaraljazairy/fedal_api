"""Serializer for the Wipecardetailing models."""
from .models import Formsubmits, Multimedia
from django.contrib.auth.models import User
from rest_framework import serializers
# from django.core.validators import URLValidator
from django.conf import settings
import logging

logger = logging.getLogger(settings.AWS_LOGGER_NAME)


class UserSerializer(serializers.ModelSerializer):
    """Serializes the User model."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class FormSubmitsSerializer(serializers.ModelSerializer):
    """Serialize the formsubmits object."""

    class Meta:
        """Specify the model to use and the fields to serialize."""

        model = Formsubmits
        fields = '__all__'
        # they extra kwargs will be returned in the view during the validation before the save.
        extra_kwargs = {
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

    # make it write_only because it doesn't need to be returned to the view
    addedbyuser = serializers.IntegerField(write_only=True)

    class Meta:
        """Specify the model to use and the fields to serialize."""
        model = Multimedia
        fields = ['id', 'title', 'type', 'uploaded_by', 'addedbyuser', 'added', 'link', 'socialmedianame']

        # they extra kwargs will be returned in the view during the validation before the save.
        extra_kwargs = {
            'title': {
                'error_messages': {
                    'required': 'Title is required',
                }
            },
            'type': {
                'error_messages': {
                    'required': 'Type field is required'
                }
            },
            'link': {
                'error_messages': {
                    'required': 'LinkUrl field is required',
                    'invalid': 'Invalid link url'
                }
            }
        }