"""Unitests for the views classes and functions"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Permission, Group
import logging

logger = logging.getLogger('spanglish')


class WordListViewTestClass(TestCase):
    """Wordlist view tests."""

    @classmethod
    def setUpClass(cls):
        """Create a test user & group with the specific permission.
        initalize the client and apiclient.
        """
        logger.debug("%s started " % cls.__name__)
        cls.api_url = 'http://127.0.0.1:8000/spanglish/words/'

        # authenticated user
        username = 'tester'
        password = 'test1234'
        email = 'tester@fedla.net'
        groupName = 'Spanglish'

        # unauthenticated user
        username2 = 'tester2'
        password2 = 'test12342'
        email2 = 'tester2@fedla.net'
        groupName2 = 'Spanglish2'


        # create users
        user = User.objects.create_user(username=username, email=email, password=password)
        user2 = User.objects.create_user(username=username2, email=email2, password=password2)
        logger.debug("user created: %s" % user)
        logger.debug("user2 created: %s" % user2)

        # create groups
        group, created = Group.objects.get_or_create(name=groupName)
        group2, created2 = Group.objects.get_or_create(name=groupName2)
        logger.debug("group: %s created: %s" % (group, created))
        logger.debug("group2: %s created: %s" % (group2, created2))

        # add user to the group
        group.user_set.add(user)
        group2.user_set.add(user2)


        # create the apiclient object
        cls.api_client = APIClient(enforce_csrf_checks=True)
        cls.api_client2 = APIClient(enforce_csrf_checks=True)

        # get token for the user1 and user2
        request = cls.api_client.post(
            '/api/token/',
            {
                'username': username,
                'password': password
            },
            format='json'
        )

        response = request.json()

        # token
        token = response['access']

        # add the token to the api_client header
        cls.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


    def test_get_language_en_200(self):
        """test the get request to the api, expects 200 response with
        content."""

        # set the url for the api with param
        uri = self.api_url + 'language/en/'
        response = self.api_client.get(uri) # make the request
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)

        self.assertEquals(status_code, 200)
        self.assertTrue(content)

    def test_get_language_en_unauthorized_401(self):
        """test the get request to the api, expects 401 response
        because the user is not authenticated.
        """

        # set the url for the api with param
        uri = self.api_url + 'language/en/'
        response = self.api_client2.get(uri) # make the request
        status_code = response.status_code
        content = response.json()
        expected_err_msg = {'detail': 'Authentication credentials were not provided.'}

        logger.debug("response: %s" % response)
        logger.debug("response content: %s" % content)

        self.assertEquals(status_code, 401)
        self.assertDictEqual(content, expected_err_msg)


    def test_get_language_error_with_no_en_404(self):
        """test the get request to the api, expects 404 response with
        content."""

        # set the url for the api with param
        uri = self.api_url + 'language/'
        response = self.api_client.get(uri) # make the request
        status_code = response.status_code

        logger.debug("response: %s" % response)

        self.assertEquals(status_code, 404)


    def test_get_language_en_content(self):
        """test the get request to the api, expects 200 response with
        content json value to match the word Hablar."""

        # set the url for the api with param
        uri = self.api_url + 'language/en/'
        response = self.api_client.get(uri) # make the request
        status_code = response.status_code
        content = response.json()

        logger.debug("content: %s" % content)

        expected_content = [
            {
                'word': 'Hablar',
                'translation': 'Talk',
                'category': 'verb',
                'language': 'English'
            }
        ]

        self.assertEquals(status_code, 200)
        self.assertDictEqual(d1=content[0], d2=expected_content[0])

    @classmethod
    def tearDownClass(cls):
        """remove the user and the group"""

        Group.objects.all().delete()
        User.objects.all().delete()