
from django.db import models
from django.contrib.auth.models import User
from .managers.multimedia_manager import MultimediaManager
from datetime import datetime
from django.conf import settings

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
APP_LABEL = 'wipecardetailing'

class LinkTypes(models.TextChoices):
    """ define the linktype of the multimedia object to one choice. """
    IMAGE = 'IMAGE', 'Image'
    VIDEO = 'VIDEO', 'Video'
    SOCIALMEDIALINK = 'SOCIALMEDIALINK', 'SocialMediaLink'

class EmailStatus(models.TextChoices):
    """
    Define the email status that will be set when sending an email.
    The defined status has to be SUCCESS, ERROR, PENDING.
    """
    SUCCESS = 'SUCCESS', 'SECCESS'
    ERROR = 'ERROR', 'ERROR'
    PENDING = 'PENDING', 'PENDING'

class Formsubmits(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    formname = models.CharField(db_column='FormName', max_length=45)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    customername = models.CharField(db_column='CustomerName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.EmailField(db_column='Email', max_length=45)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNr', max_length=45, blank=True, null=True)
    streetname = models.CharField(db_column='Street', max_length=45, blank=True, null=True)  # Field name made lowercase.
    housenumber = models.CharField(db_column='HouseNr', max_length=45, blank=True, null=True)  # Field name made lowercase.
    postcode = models.CharField(db_column='Postcode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=45, blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', max_length=254, blank=True, null=True)  # Field name made lowercase.
    submitted = models.DateTimeField(auto_now_add=False, db_column='Submitted', default=datetime.now())  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=254, blank=False, null=False,
                              choices=EmailStatus.choices, default=EmailStatus.PENDING)


    class Meta:
        managed = False
        db_table = 'FormSubmits'
        app_label = APP_LABEL

    def __str__(self):
        """Returns a representation text of the object."""
        return self.formname + ' ' + self.companyname + ' ' + str(self.submitted) + ' ' + self.status

class Multimedia(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=45, null=False, blank=False)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=15, null=False, blank=False, choices=LinkTypes.choices)  # Field name made lowercase.
    addedbyuser = models.PositiveSmallIntegerField(db_column='AddedByUser', null=False, blank=False)
    added = models.DateTimeField(auto_now_add=False, db_column='Added', default=datetime.now())  # Field name made lowercase.
    link = models.URLField(db_column='Link', unique=True, max_length=255, null=True, blank=True)
    socialmedianame = models.CharField(db_column='SocialMediaName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    file = models.ImageField(db_column='File', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'Multimedia'
        unique_together = (('title', 'type'),)
        app_label = APP_LABEL

    # because cross multiple databsase foreign keyis not allowed in django, i need to link the auth users
    # to the addedbyuser column. this is why i created this property to show the user's fullname instead of
    # the id.
    @property
    def uploaded_by(self):
        user = User.objects.get(pk=self.addedbyuser)
        return user.get_full_name()

    # return the download url of an image if the type is IMAGE.
    @property
    def download_url(self):
        if self.file:
            url = settings.DOWNLOAD_IMAGE_URI + str(self.file)
            return url


    def __str__(self):
        """Returns a representation text of the object."""
        return self.title + ' ' + self.type + ' ' + str(self.addedbyuser) + ' ' + str(self.added)

   # defined object managers
    objects = models.Manager()
    linksmanager = MultimediaManager()
