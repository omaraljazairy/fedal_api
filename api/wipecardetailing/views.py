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

        # create a new dict from the request object to append the status value with it.
        data = {k:v for k,v in request.data.items()}
        status_data = {'status': 1 }

        logger.debug("request formname: %s", data['formname'])
        status_data.update(data) # add the status of the email

        logger.debug("request: %s" % status_data)
        serializer = FormSubmitsSerializer(data=status_data)
        if serializer.is_valid():
            logger.debug("form saved")
            return Response({'Msg': 'OK'}, status=status.HTTP_201_CREATED)
        else:
            error = serializer.errors
            # convert the error to a list to get the message value
            error_value = list(error.values())
            err_msg = error_value[0][0]

            logger.error('error message: %s' % error)
            logger.error('error value: %s' % err_msg)
            logger.debug('default error message: %s', serializer.error_messages)

            return Response({'Msg': err_msg}, status=status.HTTP_400_BAD_REQUEST)