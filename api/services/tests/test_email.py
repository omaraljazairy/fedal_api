"""Unitests for the email module functions"""
from django.test import TestCase
from ..email import send
import logging

logger = logging.getLogger('email')


class EmailServiceTestClass(TestCase):
    """Formsubmits view tests."""

    @classmethod
    def setUpClass(cls):
        """initalize the general variables and methods to be used in this test. """
        cls.sender = 'test@fedal.nl'
        cls.to = [('test_to', 'tox@mytest.nl'), ('test2_to', 'toy@mytest.nl')]
        cls.cc = [('test_cc', 'ccx@mytest.nl'), ('test2_cc', 'ccy@mytest.nl')]
        cls.bcc = [('test_bcc', 'bccx@mytest.nl'), ('test2_bcc', 'bccy@mytest.nl')]
        cls.subject = "test subject"
        cls.body = "<h1>hello body</h1>"
        cls.content_type = 'html'
        cls.connection = None
        cls.headers = {'A-UNIQUE-STRING':  'mytest-1234'}
        cls.reply_to = [('test_reply', 'replyx@mytest.nl'), ('test2_reply', 'replyy@mytest.nl')]
        cls.attachments = None


    def test_send_html_success(self):
        """send an email with html content-type, expoct to get back a success response dict"""
        response = send(sender=self.sender, to=self.to, cc=self.cc, bcc=self.bcc, subject=self.subject,
                        body=self.body, content_type=self.content_type, connection=self.connection,
                        headers=self.headers, reply_to=self.reply_to, attachments=self.attachments)
        logger.debug("email response %s: " % response)
        expected_response = {'status': 'OK', 'message': "email sent"}

        self.assertEquals(response, expected_response, msg="correct response")


    def test_send_missing_sender_error(self):
        """send an email without a sender, expoct to get back an error response dict"""
        response = send(sender=None, to=self.to, cc=self.cc, bcc=self.bcc, subject=self.subject,
                        body=self.body, content_type=self.content_type, connection=self.connection,
                        headers=self.headers, reply_to=self.reply_to, attachments=self.attachments)
        logger.debug("email response %s: " % response)
        expected_response_status = 'ERROR'

        self.assertEquals(response['status'], expected_response_status, msg="correct response")


    def test_send_wrong_cc_type_error(self):
        """send a wrong cc type, expoct to get back an error response dict"""
        response = send(sender=self.sender, to=self.to, cc='foo', bcc=None, subject=self.subject,
                        body=self.body, content_type=self.content_type, connection=self.connection,
                        headers=self.headers, reply_to=self.reply_to, attachments=self.attachments)
        logger.debug("email response %s: " % response)
        expected_response_status = 'ERROR'

        self.assertEquals(response['status'], expected_response_status, msg="correct response")

    def test_send_empty_bcc_type_ok(self):
        """send an empty bcc type, expoct to get back an OK response dict"""
        response = send(sender=self.sender, to=self.to, cc=self.cc, bcc=None, subject=self.subject,
                        body=self.body, content_type=self.content_type, connection=self.connection,
                        headers=self.headers, reply_to=self.reply_to, attachments=self.attachments)
        logger.debug("email response %s: " % response)
        expected_response_status = 'OK'

        self.assertEquals(response['status'], expected_response_status, msg="correct response")


    def test_send_required_params_only_ok(self):
        """send with only the required params, expoct to get back an OK response dict"""
        response = send(sender=self.sender, to=self.to, subject=self.subject, body=self.body)
        logger.debug("email response %s: " % response)
        expected_response_status = 'OK'

        self.assertEquals(response['status'], expected_response_status, msg="correct response")


    @classmethod
    def tearDownClass(cls):
        """teardown any initialized object"""
        logger.debug("tearing down formsubmit view tests")
