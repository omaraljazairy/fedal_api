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
    file = serializers.ImageField(write_only=True, required=False)
    type = serializers.CharField(required=True)

    def validate(self, data):
        """
        custom valitions for the type image and the file field.

        If the type field is image and there is no file, return an error.
        """

        logger.debug("Serializers validation multimedia data: %s" % data)
        if data.get('type', False) == 'IMAGE':
            if not data.get('file', False):
                #if file isn't available, rais an exception
                raise serializers.ValidationError('Image type should have an image file')
            else:
                return data
        else:
            return data

    class Meta:
        """Specify the model to use and the fields to serialize."""
        model = Multimedia
        fields = [
            'id',
            'title',
            'type',
            'uploaded_by',
            'addedbyuser',
            'added',
            'socialmedialink',
            'socialmedianame',
            'file',
            'download_url'
        ]

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
            'socialmedialink': {
                'error_messages': {
                    'invalid': 'Invalid link url'
                }
            }
        }