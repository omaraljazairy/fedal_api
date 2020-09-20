"""Unitests for the views classes and functions"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework_api_key.models import APIKey
from PIL import Image
import io
import logging

logger = logging.getLogger('wipecardetailing')


class MultimediaViewTestClass(TestCase):
    """Multmedia view tests."""

    @classmethod
    def setUpClass(cls):
        """Create a test user & group with the specific permission.
        initalize the client and apiclient.
        Also create an api key for the get requests
        """
        logger.debug("%s started " % cls.__name__)
        cls.api_url = 'http://127.0.0.1:8000/wipecardetailing/multimedia/'
        cls.api_url_post = 'http://127.0.0.1:8000/wipecardetailing/multimedia/post/'
        cls.api_url_detail = 'http://127.0.0.1:8000/wipecardetailing/multimedia/detail/'

        # authenticated user
        username = 'tester'
        password = 'test1234'
        email = 'tester@fedal.net'
        groupName = 'Wipecardetailing'

        # unauthenticated user
        username2 = 'tester2'
        password2 = 'test12342'
        email2 = 'tester2@fedal.net'
        groupName2 = 'Wipcardetailing'


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

        # create an imagefile to be saved and used for attachments.
        cls.attachment_image = io.BytesIO()  # tempfile.NamedTemporaryFile(suffix='.jpg')
        cls.attachment_image.name = 'testImage.jpg'
        image_file = Image.new('RGB', (30, 10), (255, 214, 107))
        image_file.save(cls.attachment_image, 'jpeg')

        cls.attachment_image.seek(0)

        # create a token
        api_key, key = APIKey.objects.create_key(name="wipecardetailings")
        logger.debug("generated api-key: %s" % api_key)
        logger.debug("generated key: %s" % key)

        # create the apiclient object
        cls.api_client_apikey = APIClient(enforce_csrf_checks=True)
        cls.api_client_jwt = APIClient(enforce_csrf_checks=True)
        cls.api_client2_jwt = APIClient(enforce_csrf_checks=True)

        # get token for the user1
        request = cls.api_client_jwt.post(
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

        # add the token to the api_client_jwt authenticated user header
        cls.api_client_jwt.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # add the api-key to the header of the api_client which is for get
        # requests only
        cls.api_client_apikey.credentials(HTTP_X_API_KEY=key)


    def test_get_multimedialinks_authenticated_200(self):
        """
        test the get request to the api, expects 200 response.
        """

        response = self.api_client_apikey.get(self.api_url) # make the request
        status_code = response.status_code

        logger.debug("response: %s" % response)

        self.assertEquals(status_code, 200)


    def test_get_multimedialinks_unauthenticated_401(self):
        """
        test the get request to the api with an unauthenticated user,
        expects 401 response.
        """

        response = self.api_client2_jwt.get(self.api_url) # make the request
        status_code = response.status_code

        logger.debug("response: %s" % response)

        self.assertEquals(status_code, 401)

    def test_get_all_multimedia_content_200(self):
        """
        test the get request to the api with no params.
        expects 200 http response with json content.
        the keys of one of the object responses should match
        the expected keys.
        """

        response = self.api_client_apikey.get(self.api_url) # make the request
        status_code = response.status_code
        content = response.json()

        logger.debug("content: %s" % content)

        response_keys = list(content[0].keys())
        expected_keys = sorted(
            [
                'id',
                'title',
                'type',
                'uploaded_by',
                'added',
                'link',
                'socialmedianame'
            ]
        )

        self.assertEquals(status_code, 200)
        self.assertEquals(response_keys, expected_keys)
        #self.assertDictEqual(d1=content[0], d2=expected_content[0])


    def test_get_all_multimedia_content_200(self):
        """
        make a et request with no params and expect http esponse 200 with
        json content of three objects.
        """

        response = self.api_client_apikey.get(self.api_url) # make the request
        status_code = response.status_code
        content = response.json()

        logger.debug("content: %s" % content)

        # expected_content = [
        #     {
        #         "id": 1,
        #         "title": "First Car Wash",
        #         "type": "Image",
        #         "addedbyuser": 2,
        #         "added": "2020-07-26T09:55:57Z",
        #         "link": "https://fedal.net/carwash.jpg",
        #         "socialmedianame": "null"
        #     },
        #     {
        #         "id": 2,
        #         "title": "Car Wash2",
        #         "type": "SocialMediaLink",
        #         "addedbyuser": 3,
        #         "added": "2020-07-26T09:57:15Z",
        #         "link": "https://youtube.com/wejhsvgerv32vg",
        #         "socialmedianame": "youtube"
        #     },
        #     {
        #         "pk": 3,
        #         "title": "Tankstation Cleaner",
        #         "type": "SocialMediaLink",
        #         "addedbyuser": 2,
        #         "added": "2020-07-26T09:58:19Z",
        #         "link": "https://facebook.com/wejhsvgerv32vg",
        #         "socialmedianame": "facebook"
        #     }
        # ]
        self.assertEquals(status_code, 200)
        # self.assertEquals(len(content), 3)
        self.assertGreaterEqual(len(content), 3)


    def test_get_multimedia_wuith_querystring_200(self):
        """
        make a get request with params socialmedianame is facebook and type
        is SocialMediaLink. expect to get one object back that matches the
        expected object. Type is json content and status code is 200
        """

        params = {'socialmedianame': 'facebook', 'type': 'SocialMediaLink'}
        response = self.api_client_apikey.get(self.api_url, data=params) # make the request
        status_code = response.status_code
        content = response.json()
        data = response.data

        logger.debug("content: %s" % content)
        logger.debug("data content: %s" % data)

        expected_content = [
            {
                "id": 3,
                "download_url": None,
                "title": "Tankstation Cleaner",
                "type": "SocialMediaLink",
                "uploaded_by": "Omar Aljazairy",
                "added": "2020-07-26 11:58:19+0200",
                "link": "https://facebook.com/wejhsvgerv32vg",
                "socialmedianame": "facebook",
            }
        ]
        self.assertEquals(status_code, 200)
        self.assertEquals(len(content), 1)
        self.assertDictEqual(expected_content[0], content[0])


    def test_post_multimedia_valid_request_params_201(self):
        """
        post a valid link with all required parameters.
        expect to get back response 201.
        """

        data = {
            'title': 'a view to kill',
            'type': 'SOCIALMEDIALINK',
            'link': 'http://fedal.nl',
            'socialmedianame': 'facebook'
        }

        response = self.api_client_jwt.post(self.api_url_post, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_201_CREATED)
        self.assertEquals(response['Content-Type'], 'application/json')


    def test_post_multimedia_invalid_url_link_400(self):
        """
        post an invalid url link with all required parameters.
        expect to get back response 400.
        """

        data = {
            'title': 'an invalid link',
            'type': 'SocialMediaLink',
            'link': 'invalid_link',
            'socialmedianame': 'facebook'
        }

        expected_error_msg = {'Msg': 'Invalid link url'}

        response = self.api_client_jwt.post(self.api_url_post, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertDictEqual(content, expected_error_msg)


    def test_post_multimedia_valid_request_uppercase_params_201(self):
        """
        post a valid request with all required parameters with uppercase letter.
        expect to get back response 201.
        """

        data = {
            'Title': 'a view to kill 2',
            'Type': 'SOCIALMEDIALINK',
            'Link': 'http://fedal.nl',
            'Socialmedianame': 'facebook'
        }

        response = self.api_client_jwt.post(self.api_url_post, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_201_CREATED)
        self.assertEquals(response['Content-Type'], 'application/json')


    def xtest_post_multimedia_valid_request_lowercase_values_201(self):
        """
        post a valid request with all required parameters with lowercase letters.
        expect to get back response 201.
        """

        data = {
            'Title': 'a view to kill 4',
            'Type': 'socialmedialink',
            'Link': 'http://fedal.nl',
            'Socialmedianame': 'facebook'
        }

        response = self.api_client_jwt.post(self.api_url_post, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_201_CREATED)
        self.assertEquals(response['Content-Type'], 'application/json')

    def test_post_multimedia_invalid_request_type_image_without_file_400(self):
        """
        post a post request with all required parameters and type is image but without
        sending an image file. expect response 400 bad request
        """

        data = {
            'Title': 'a view to kill 3',
            'Type': 'Image',
            'Link': 'http://fedal.nl/3',
            'Socialmedianame': 'facebook'
        }

        response = self.api_client_jwt.post(self.api_url_post, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response['Content-Type'], 'application/json')

    def test_post_multimedia_valid_request_type_image_with_file_201(self):
        """
        post a post request with all required parameters and type is image with
        an image file. expect response 201
        """

        data = {
            'Title': 'a view to kill 3',
            'Type': 'Image',
            'Link': 'http://fedal.nl/3',
            'Socialmedianame': 'facebook',
            'file': self.attachment_image
        }

        response = self.api_client_jwt.post(self.api_url_post, data=data, format='multipart')
        status_code = response.status_code
        content = response.json()
        expected_keys = sorted(['Msg', 'Id', 'Link'])
        returned_keys = sorted(list(content.keys()))
        returned_values = all(list(content.values()))

        #expected_download_url = 'http://192.168.178.25//media/' + self.attachment_image.__dict__
        # expected_esponse_content = {'Msg': 'OK', 'Id': content['Id'], 'Link': expected_download_url}

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)
        logger.debug("returned_values: %s" % returned_values)
        #logger.debug("attachment name: %s" % self.attachment_image.__dict__)

        self.assertEquals(status_code, status.HTTP_201_CREATED)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(expected_keys, returned_keys)
        self.assertTrue(returned_values) # expect all values to be True


    def test_post_multimedia_with_apikey_unauthenticated_401(self):
        """
        post a valid link with apikey authentication only.
        expect to get back response 401.
        """

        data = {
            'title': 'a view to kill',
            'type': 'SocialMediaLink',
            'link': 'http://fedal.nl',
            'socialmedianame': 'facebook'
        }

        response = self.api_client_apikey.post(self.api_url_post, data=data)
        status_code = response.status_code
        content = response.data

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_401_UNAUTHORIZED)


    def test_retrieve_multimedia_200(self):
        """
        Make Get request with the id in the url only that returns one item
        with status code 200.
        """
        url = self.api_url_detail + '1/'
        response = self.api_client_jwt.get(url)
        status_code = response.status_code
        content = response.data if status_code == 200 else None

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, 200)


    def test_retrieve_multimedia_apikey_200(self):
        """
        Make Get request with the id using the api-key, expects to returns
        one item with status code 200.
        """
        url = self.api_url_detail + '1/'
        response = self.api_client_apikey.get(url)
        status_code = response.status_code
        content = response.data if status_code == 200 else None

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, 200)


    def test_patch_multimedia_200(self):
        """
        Make a Patch request with a change of the title. Expect success
        with status code 200
        """

        url = self.api_url_detail + '4/'
        data = {'title': 'Tankstation Shell 2 Cleaner'}
        response = self.api_client_jwt.patch(url, data)
        status_code = response.status_code
        content = response.data

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, status.HTTP_200_OK)


    def test_put_multimedia_not_allowed_405(self):
        """
        Make a Put request with a change of the title. Expect an error
        with status code 405 because Put is not allowed
        """

        url = self.api_url_detail + '4/'
        data = {'title': 'Tankstation Shell 4 Cleaner'}
        response = self.api_client_jwt.put(url, data)
        status_code = response.status_code
        content = response.data

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_multimedia_apikey_unautherized_401(self):
        """
        Make a Patch request with an apikey. Expect error
        with status code 401
        """

        url = self.api_url_detail + '4/'
        data = {'title': 'Tankstation Shell 3 Cleaner'}
        response = self.api_client_apikey.patch(url, data)
        status_code = response.status_code
        content = response.data

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_multimedia_200(self):
        """
        Make a Delete request for the id 5. Expect success
        with status code 200.
        """

        url = self.api_url_detail + '5/'
        response = self.api_client_jwt.delete(url)
        status_code = response.status_code
        content = response.data

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_multimedia_apikey_unautherized_401(self):
        """
        Make a Delete request for the id 5 with an apikey only. Expect error
        with response 401.
        """

        url = self.api_url_detail + '5/'
        response = self.api_client_apikey.delete(url)
        status_code = response.status_code
        content = response.data

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEqual(status_code, status.HTTP_401_UNAUTHORIZED)

    @classmethod
    def tearDownClass(cls):
        """remove the user and the group"""

        Group.objects.all().delete()
        User.objects.all().delete()