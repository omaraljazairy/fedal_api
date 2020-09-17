from .models import Formsubmits, Multimedia
from .serializers import FormSubmitsSerializer, MultimediaSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from api.throttles import WipecardetailingRateThrottle
from django.conf import settings
from django.core.cache import cache
from services.email import send
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from decorators.timem import time_memory
import logging

CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
# logger = logging.getLogger('wipecardetailing')
logger = logging.getLogger(settings.AWS_LOGGER_NAME)

class FormsubmitsView(generics.ListCreateAPIView):
    """ Get all the form data submitted. """
    permission_classes = [HasAPIKey]
    throttle_classes = (WipecardetailingRateThrottle,)
    name  = 'formsubmit-listcreate'
    serializer_class = FormSubmitsSerializer

    @swagger_auto_schema(security=[{'ApiKeyAuth': [
        'Uses the X-API-KEY param name in the header.']}],)
    def get(self, request, *args, **kwargs):
        """Takes no aguments at the moment and returns all the submitted forms. """

        logger.debug("request received: %s" % request.GET)

        queryset = Formsubmits.objects.all()
        serializer = FormSubmitsSerializer(queryset, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[{'ApiKeyAuth': [
        'Uses the X-API-KEY param name in the header.']}],)
    def post(self, request, *args, **kwargs):
        """
        Saves the submitted form data in the database and send it as an email.
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


class MultmediaListView(generics.GenericAPIView):
    """
    Takes no or multiple parametes and returns a list of the
    multimedia items. It requires the api-key only to fetch data.
    """

    permission_classes = [HasAPIKey]
    throttle_classes = (WipecardetailingRateThrottle,)
    serializer_class = MultimediaSerializer
    name  = 'multimedia-list'

    @swagger_auto_schema(security=[{'ApiKeyAuth': [
        'Uses the X-API-KEY param name in the header.']}],)
    @time_memory
    def get(self, request, *args, **kwargs):
        """
        :param request: non or multiple params to form the queryset filter.
        :param args: non expected
        :param kwargs: non expected
        :return: json response with the list of items or one item
        """

        # create a dict object from the received parameters which have no
        # empty value and in the expected valid parametes.
        # better to do this validation here in the view before reaching the serializer.
        valid_params = ['id', 'title', 'type', 'socialmedianame']
        query_string = {k.lower() :v for k,v in request.query_params.items() if v and k in valid_params}
        logger.debug("request received: %s" % request.query_params)

        logger.debug("query_string: %s" % query_string)

        #queryset = Multimedia.objects.filter(type=query_string['type'])
        queryset = Multimedia.linksmanager.get_links(**query_string)
        serialized = MultimediaSerializer(queryset, many=True)

        data = {'data': serialized.data}
        logger.debug("queryset: %s" % data)

        return Response(serialized.data, status=status.HTTP_200_OK)


class MultimediaCreateView(generics.CreateAPIView):
    """Creates a socialmedia link record.

    It is restricted to authenticated users only. User must
    login first to upload an link. This is not for uploading images.
    The authenticated user pk will be used by the addedbyuser attribute.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = (WipecardetailingRateThrottle,)
    serializer_class = MultimediaSerializer
    name  = 'multimedia-list'
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(security=[{'Bearer': [
        'Uses the Athentication param name in the header with the Bearer Token as value.']}],)
    def post(self, request, *args, **kwargs):
        """Saves the socialmedia link for Authenticated users only.

        Get the userid from the request.
        copy the request object because it is immutable. We need to provide the
        addedbyuser attribute with the userid.
        create the object and use the userid as the addbyuser attribute before
        passing it to the serializer.
        :return 201 if success, otherwise 404 with an error message.
        """

        # create a new dict from the request object to append the status value with it.
        posted_data = {k.lower(): v for k, v in request.data.items()}
        logger.debug('data received: %s' % posted_data)

        # if the type is Image, there should then be a file sent in the post.
        # make the link value the url of the file to be downloaded.
        # otherwise if the type is image and there is no image file sent, return 400
        # if posted_data['type'] == 'Image':
        #     if request.data.get('file', None):
        #         #posted_data['link'] = 'http://localhost/' + request.data['file']
        #         file_obj = request.data['file']
        #         logger.debug('file received: %s' % file_obj.__dict__)
        #         logger.debug('file name received: %s' % file_obj._name)
        #         posted_data['link'] = 'http://localhost/' + file_obj._name
        #     else:
        #         err_msg = "type Image but there is no image submitted"
        #         return Response({'Msg': err_msg}, status=status.HTTP_400_BAD_REQUEST)

        # get the authenticated user from the request object.
        user = request.user
        logger.debug("user received: %s" % user)
        logger.debug("user pk received: %s" % user.pk)
        if posted_data.get('type', False):
            posted_data['type'] = posted_data['type'].upper()

        # append the addedbyuser key to the posted_data with the userid value.
        posted_data.update({'addedbyuser': 2})
        logger.debug("final posted_data: %s" % posted_data)

        serializer = MultimediaSerializer(data=posted_data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            logger.debug("data is valid and saved: %s", data)
            msg = {
                'Msg': 'OK',
                'Id': data['id'],
                'Link': data['link']
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            error = serializer.errors
            # convert the error to a list to get the message value
            error_value = list(error.values())
            err_msg = error_value[0][0]

            logger.error('error message: %s' % error)
            logger.error('error value: %s' % err_msg)
            logger.debug('default error message: %s', serializer.error_messages)

            return Response({'Msg': err_msg}, status=status.HTTP_400_BAD_REQUEST)


class MultimediaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Takes a Get, Patch and Delete for authenticated users.

    use a get request with the id of the object in the url to retrieve
    the object details.

    also takes a patch and delete requests to only users who have the add and
    delete rights.

    the put request is not allowed at this moment.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer

    def put(self, request, *args, **kwargs):
        """Returns 405 because it's not allowed. use patch instead"""

        return Response({'Msg':'Use PATCH for updates'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)