from django.db import models

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
    submitted = models.DateTimeField(auto_now_add=True, db_column='Submitted')  # Field name made lowercase.
    # status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=254, blank=False, null=False, default='PENDING')


    class Meta:
        managed = False
        db_table = 'FormSubmits'
        app_label = APP_LABEL

class Multimedia(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=45)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=15)  # Field name made lowercase.
    addedbyuser = models.CharField(db_column='AddedByUser', max_length=45)  # Field name made lowercase.
    added = models.DateTimeField(auto_now_add=True, db_column='Added')  # Field name made lowercase.
    link = models.CharField(db_column='Link', unique=True, max_length=255)  # Field name made lowercase.
    socialmedianame = models.CharField(db_column='SocialMediaName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Multimedia'
        unique_together = (('title', 'type'),)
        app_label = APP_LABEL
