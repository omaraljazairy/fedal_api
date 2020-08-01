from .models import Formsubmits
from .serializers import FormSubmitsSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from api.throttles import WipecardetailingRateThrottle
from django.conf import settings
from django.core.cache import cache
from services.email import send
import logging

CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
logger = logging.getLogger('wipecardetailing')


class FormsubmitsView(generics.ListCreateAPIView):
    """ post and get requests to the form without any restrictions. """
    permission_classes = (AllowAny,)
    throttle_classes = (WipecardetailingRateThrottle,)
    name  = 'formsubmit-listcreate'
    queryset = Formsubmits.objects.all()
    serializer_class = FormSubmitsSerializer

    def post(self, request, *args, **kwargs):
        """create a formsubmit object with the status value depending on the email send result if required.
        if the email is sent successfully, the status of the formsubmit will be true, otherwise false.
        """

        # create a new dict from the request object to append the status value with it.
        data = {k:v for k,v in request.data.items()}
        logger.debug('data: %s' % data)

        # create a dict for the email send function.
        email_data = {
            'sender': settings.EMAIL_HOST_USER,
            'subject': data.get('formname',False),
            'body': data.get('message', False),
            'to': [('Omar', 'omar@fedal.nl'),],
            'content_type': 'html'
        }

        logger.debug('email data: %s' % email_data)
        # if any of the values in the eail_data is not True, the status will be 0
        if all(email_data.values()):
            email_response = send(**email_data)
            if email_response['status'] == 'OK':
                status_data = {'status': 1 }
            else:
                status_data = {'status': 0}
        else:
            status_data = {'status': 0}

        status_data.update(data) # add the status of the email

        logger.debug("request: %s" % status_data)
        serializer = FormSubmitsSerializer(data=status_data)
        if serializer.is_valid():
            serializer.save()
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