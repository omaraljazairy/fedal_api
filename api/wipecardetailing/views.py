from django.shortcuts import render

# Create your views here.
from .models import Formsubmits
from .serializers import FormSubmitsSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from api.throttles import WipecardetailingRateThrottle
from django.conf import settings
from django.core.cache import cache
import logging


CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
logger = logging.getLogger('wipecardetailing')


class FormsubmitsView(generics.ListCreateAPIView):
    """ post and get requests to the form without any restrictions. """
    permission_classes = (AllowAny,)
    name  = 'formsubmit-listcreate'
    queryset = Formsubmits.objects.all()
    serializer_class = FormSubmitsSerializer

    def post(self, request, *args, **kwargs):
        """override the post because the status value depneds on the email"""

        form_data = request.data
        required_fields = ('formname', 'email')
        # if set(form_data.keys()).intersection(required_fields):
        #     logger.debug('missing required field')
        #     return Response({'Msg': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug("request: %s" % request.data)
        serializer = FormSubmitsSerializer(data=form_data)
        if serializer.is_valid():
            logger.debug("form_saved")
            return Response({'Msg': 'OK'}, status=status.HTTP_201_CREATED)
        else:
            logger.error('form save: %s' % serializer.error_messages)
            return Response({'Msg': serializer.error_messages['required']}, status=status.HTTP_400_BAD_REQUEST)