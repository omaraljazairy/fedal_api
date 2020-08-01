"""Unitests for the views classes and functions"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import logging

logger = logging.getLogger('wipecardetailing')


class FormsubmitsViewTestClass(TestCase):
    """Formsubmits view tests."""

    @classmethod
    def setUpClass(cls):
        """initalize the apiclient and the api irl. """

        logger.debug("%s started " % cls.__name__)
        cls.api_url = 'http://127.0.0.1:8000/wipecardetailing/formsubmit/'

        # create the apiclient object
        cls.api_client = APIClient(enforce_csrf_checks=True)

    def test_get_three_formsubmits_200(self):
        """test the get request to the api, expects to get 3 objects in json response
        format with http 200 response.
        """

        # set the url for the api with param
        response = self.api_client.get(self.api_url)  # make the GET request
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response['Content-Type'])
        logger.debug("response content: %s" % content)

        self.assertEquals(status_code, status.HTTP_200_OK)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(len(content), 3)

    def test_post_formsubmit_201(self):
        """post request to create a new formsubmit, expect to get back
        json response with statuscode 201"""

        data = {
            'formname': 'TanStation',
            'email': 'bla@test.com',
            'companyname': 'Foo-Bar co',
        }
        response = self.api_client.post(self.api_url, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_201_CREATED)
        self.assertEquals(response['Content-Type'], 'application/json')

    def test_post_formsubmit_mising_email_400(self):
        """post request to create a new formsubmit without an email, expect to get back
        and error with statuscode 400"""

        data = {
            'formname': 'TanStation',
            'companyname': 'Foo-Bar co',
        }
        response = self.api_client.post(self.api_url, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(content['Msg'], 'Email field is required')

    def test_post_formsubmit_invalid_email_400(self):
        """post request to create a new formsubmit without an invalid email, expect to get back
        and error with statuscode 400"""

        data = {
            'formname': 'TanStation',
            'companyname': 'Foo-Bar co',
            'email': 'foobar'
        }
        response = self.api_client.post(self.api_url, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(content['Msg'], 'Invalid email')

    def test_post_formsubmit_mising_formname_400(self):
        """post request to create a new formsubmit without a formname, expect to get back
        and error with statuscode 400"""

        data = {
            'email': 'foo@bar.com',
            'companyname': 'Foo-Bar co',
        }
        response = self.api_client.post(self.api_url, data=data)
        status_code = response.status_code
        content = response.json()

        logger.debug("response: %s" % response)
        logger.debug("content: %s" % content)

        self.assertEquals(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(content['Msg'], 'Formname field is required')

    @classmethod
    def tearDownClass(cls):
        """teardown any initialized object"""
        logger.debug("tearing down formsubmit view tests")
