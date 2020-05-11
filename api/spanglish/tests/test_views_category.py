"""Unitests for the views classes and functions"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission, Group
from ..models import Category
import logging

logger = logging.getLogger('spanglish')


class CategoryViewTestClass(TestCase):
    """Wordlist view tests."""

    @classmethod
    def setUpClass(cls):
        """Create a test user & group with the specific permission.
        initalize the client and apiclient.
        """
        logger.debug("%s started " % cls.__name__)
        cls.api_url = 'http://127.0.0.1:8000/spanglish/category/'

        # create permissions
        # first get the contenttype of the model
        content_type = ContentType.objects.get_for_model(Category)
        add_permission, created = Permission.objects.get_or_create(
            codename='add_category',
            name='Can add category',
            content_type=content_type
        )
        change_permission, created = Permission.objects.get_or_create(
            codename='change_category',
            name='Can change category',
            content_type=content_type
        )
        delete_permission, created = Permission.objects.get_or_create(
            codename='delete_category',
            name='Can delete category',
            content_type=content_type
        )

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

        # add permissings to group
        group.permissions.add(add_permission)
        group.permissions.add(delete_permission)
        group.permissions.add(change_permission)

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


    def test_get_all_categories_200(self):
        """test the get request to the api, expects 200 response with
        content."""

        # set the url for the api with param
        uri = self.api_url
        response = self.api_client.get(uri) # make the request
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)

        self.assertEquals(status_code, 200)
        self.assertTrue(content)

    def test_get_categories_unauthorized_401(self):
        """test the get request to the api, expects 401 response
        because the user is not authenticated.
        """

        # set the url for the api with param
        uri = self.api_url
        response = self.api_client2.get(uri) # make the request
        status_code = response.status_code
        content = response.json()
        expected_err_msg = {
            'detail': 'Authentication credentials were not provided.'
        }

        logger.debug("response: %s" % response)
        logger.debug("response content: %s" % content)

        self.assertEquals(status_code, 401)
        self.assertDictEqual(content, expected_err_msg)


    def test_get_category_error_with_unknow_param_404(self):
        """test the get request to the api with an unknown param,
        expects 404 response with content."""

        # set the url for the api with param
        uri = self.api_url + 'all/'
        response = self.api_client.get(uri) # make the request
        status_code = response.status_code

        logger.debug("response: %s" % response)

        self.assertEquals(status_code, 404)


    def test_get_category_with_content(self):
        """test the get request to the api to get category id 1.
        expects 200 response with content json value to match
        the name Verb."""

        # set the url for the api with param
        uri = self.api_url + '1/'
        response = self.api_client.get(uri) # make the request
        status_code = response.status_code
        content = response.json()

        logger.debug("content: %s" % content)

        expected_content = {
                'id': 1,
                'name': 'verb',
                'created': '2020-03-15T14:29:37+01:00'
        }


        self.assertEquals(status_code, 200)
        self.assertDictEqual(d1=content, d2=expected_content)


    def test_create_category_201(self):
        """post request to create a new category, expect to get back
        json response with statuscode 201"""

        data = {'name':'foo'}
        response = self.api_client.post(self.api_url, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(201, status_code)

    def test_create_existing_category_400(self):
        """post an existing category"""

        data = {'name':'verb'}
        response = self.api_client.post(self.api_url, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(400, status_code)
        self.assertEquals({'name': ['category with this name already exists.']}, content)


    def test_put_category_200(self):
        """update a category by calling the put action. expects response 200"""

        uri = self.api_url + '2/'
        response = self.api_client.put(uri, data={'name': 'bar2'})
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(200, status_code)

    def test_delete_category_204(self):
        """delete a category and expect 204"""

        uri = self.api_url + '3/'
        response = self.api_client.delete(uri, data={})
        status_code = response.status_code

        logger.debug("response: %s" % response)

        self.assertEquals(204, status_code)


    @classmethod
    def tearDownClass(cls):
        """remove the user and the group"""

        Permission.objects.all().delete()
        Group.objects.all().delete()
        User.objects.all().delete()