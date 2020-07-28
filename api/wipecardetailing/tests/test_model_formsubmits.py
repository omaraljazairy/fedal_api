"""Simple Unitesting for the Language model."""

from django.test import TestCase
from ..models import Formsubmits
import logging

logger = logging.getLogger('wipecardetailing')


class FormsubmitModelTestClass(TestCase):
    """Test the Formsubmits model"""

    @classmethod
    def setUpClass(cls):
        """Run at the start of the test of this class."""
        logger.debug("setUpClass started")

    def test_get_formsubmit_formname_contact(self):
        """get the 1st formsubmit and expect the formname to be Contact"""

        form_submit = Formsubmits.objects.get(pk=1)
        logger.debug("formsubmit: %s" % form_submit)
        logger.debug("form_submit name: %s" % form_submit.formname)

        self.assertEquals(form_submit.formname, 'Contact')


    def test_create_formsubmits_required_fields_only(self):
        """ test the creation of the submitform doesn't require all attributes."""
        form_sumit = Formsubmits.objects.create(
            formname='Parking',
            companyname='my test company',
            email='foo@fedal.nl',
            status=1
        )
        form_sumit.save()

        logger.debug("formsubmit created %s" % form_sumit)
        logger.debug("form_submit email: %s" % form_sumit.email)

        self.assertIsInstance(form_sumit, Formsubmits)


    def test_applabel_formsumbit_spanglish(self):
        """expect the applabel to be wipecardetailing."""

        form_submit = Formsubmits.objects.get(pk=1)
        applabel = str(form_submit._meta.app_label)

        logger.debug('applabel: %s' % applabel)

        self.assertEquals(applabel, 'wipecardetailing')


    @classmethod
    def tearDownClass(cls):
        """Run after all tests are done."""
        logger.debug("tearDownClass started")
