from .models import Formsubmits
from .serializers import FormSubmitsSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from api.throttles import WipecardetailingRateThrottle
from django.conf import settings
from django.core.cache import cache
from services.email import send
from rest_framework_api_key.permissions import HasAPIKey
from drf_yasg.utils import swagger_auto_schema
import logging

CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
# logger = logging.getLogger('wipecardetailing')
logger = logging.getLogger(settings.AWS_LOGGER_NAME)

class FormsubmitsView(generics.ListCreateAPIView):
    """ post and get requests to the form without any restrictions. """
    permission_classes = [HasAPIKey]
    throttle_classes = (WipecardetailingRateThrottle,)
    name  = 'formsubmit-listcreate'
    serializer_class = FormSubmitsSerializer

    @swagger_auto_schema(operation_description="Get all the form data submitted",
                         security=[
                             {
                                 'ApiKeyAuth':
                                 [
                                     'Uses the X-API-KEY param name in the header.'
                                 ]
                             }
                         ],
                         )
    def get(self, request, *args, **kwargs):
        """override the get to customize the data returned and add logging. """

        logger.debug("request received: %s" % request.GET)

        queryset = Formsubmits.objects.all()
        serializer = FormSubmitsSerializer(queryset, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Posts a form data",
                         security=[
                             {
                                 'ApiKeyAuth':
                                     [
                                         'Uses the X-API-KEY param name in the header.'
                                     ]
                             }
                         ],
                         )
    def post(self, request, *args, **kwargs):
        """save the submitted form data in the database and send it as an email.
        The http statuscode returned will be 201 if success.
        """

        # create a new dict from the request object to append the status value with it.
        data = {k:v for k,v in request.data.items()}
        logger.debug('form data received: %s' % data)

        # get the emails to from the EMAIL_TO environment variable
        # the EMAIL_TO variable will be a string with a name and email
        # split by a comma. each name and email combination will be seperated
        # by a ; example foo,foo@foo.com;bar@bar.com
        to = settings.EMAIL_TO
        # convert the EMAIL_TO string to a list of tuples.
        email_to = list(tuple(t.split(",")) for t in to.split(";"))

        # create a dict for the email send function.
        email_data = {
            'sender': settings.EMAIL_HOST_USER,
            'subject': data.get('formname',False),
            'body': data.get('message', False),
            'to': email_to, # [('Omar', 'omar@fedal.nl'),],
            'content_type': 'html'
        }

        # if any of the values in the eail_data is not True, the status will be 0
        if all(email_data.values()):
            email_response = send(**email_data)
            # email_response = {'status': 'OK'}
            if email_response['status'] == 'OK':
                status_data = {'status': 'SUCCESS'}
            else:
                status_data = {'status': 'ERROR'}
        else:
            status_data = {'status': 'ERROR'}

        status_data.update(data) # add the status of the email
        logger.debug("email request status: %s" % status_data)

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