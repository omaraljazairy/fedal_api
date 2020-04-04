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
        username = 'tester'
        password = 'test1234'
        email = 'tester@fedla.net'
        groupName = 'Spanglish'

        # create user, group
        user = User.objects.create_user(username=username, email=email, password=password)
        logger.debug("user created: %s" % user)

        group, created = Group.objects.get_or_create(name=groupName)
        logger.debug("group: %s created: %s" % (group, created))

        # add user to the group
        group.user_set.add(user)


        # create the apiclient object
        cls.api_client = APIClient(enforce_csrf_checks=True)

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
        logger.debug("status_code: %s" % status_code)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, 200)
        self.assertTrue(content)

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