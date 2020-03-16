"""This is an auto-generated Django model module.

You'll have to do the following manually to clean this up:
* Rearrange models' order
* Make sure each model has one field with primary_key=True
* Make sure each ForeignKey has `on_delete` set to the desired behavior.
* Remove `managed = False` lines if you wish to allow Django to create,
* modify, and delete the table
Feel free to rename the models, but don't rename db_table values
or field names.
"""

from django.db import models
from .managers import WordsManager


APP_LABEL = 'spanglish'


class Category(models.Model):
    """Category types of the words or sentences.

    for example Verb, Months, Days etc.
    """

    id = models.AutoField(db_column='Id', primary_key=True)
    created = models.DateTimeField(db_column='Created')
    name = models.CharField(db_column='Name', unique=True, max_length=45)

    class Meta:
        """additional settings for the Category object."""

        managed = False
        db_table = 'Category'
        app_label = APP_LABEL


class Language(models.Model):
    """Language of the translated spanish word."""

    id = models.AutoField(db_column='Id', primary_key=True)
    name = models.CharField(db_column='Name', unique=True, max_length=45)
    iso1 = models.CharField(db_column='ISO1', max_length=45)
    added = models.DateTimeField(db_column='Added', blank=True, null=True)

    class Meta:
        """additional settings for the Language object."""

        managed = False
        db_table = 'Language'
        app_label = APP_LABEL


class Sentence(models.Model):
    """Spanish sentence object with a category."""

    id = models.AutoField(db_column='Id', primary_key=True)
    sentence = models.CharField(db_column='Sentence', max_length=255)
    categoryid = models.IntegerField(db_column='CategoryId',
                                     blank=False, null=False)
    added = models.DateTimeField(db_column='Added')

    class Meta:
        """additional settings for the Sentence object."""

        managed = False
        db_table = 'Sentence'
        app_label = APP_LABEL


class Translation(models.Model):
    """Word or Sentence translation with a specific language."""

    id = models.AutoField(db_column='Id', primary_key=True)
    languageid = models.IntegerField(db_column='LanguageId')
    wordid = models.IntegerField(db_column='WordId', blank=True, null=True)
    sentenceid = models.IntegerField(db_column='SentenceId',
                                     blank=True, null=True)
    added = models.DateTimeField(db_column='Added')
    translation = models.CharField(db_column='Translation', max_length=255)

    class Meta:
        """additional settings for the Translation object."""

        managed = False
        db_table = 'Translation'
        unique_together = (('wordid', 'translation'),
                           ('sentenceid', 'translation'),)
        app_label = APP_LABEL


class Verb(models.Model):
    """Verb object which is related to the word of category type verb."""

    id = models.AutoField(db_column='Id', primary_key=True)
    wordid = models.IntegerField(db_column='WordId')
    verb = models.CharField(db_column='Verb', max_length=45)
    tense = models.CharField(db_column='Tense', max_length=7)
    pronouns = models.CharField(db_column='Pronouns', max_length=15)
    added = models.DateTimeField(db_column='Added')

    class Meta:
        """additional settings for the Verb object."""

        managed = False
        db_table = 'Verb'
        unique_together = (('wordid', 'pronouns'),)
        app_label = APP_LABEL


class Word(models.Model):
    """The word object that contains a category type."""

    id = models.AutoField(db_column='Id', primary_key=True)
    word = models.CharField(db_column='Word', unique=True, max_length=45)
    categoryid = models.IntegerField(db_column='CategoryId')
    added = models.DateTimeField(db_column='Added')

    class Meta:
        """additional settings for the Word object."""

        managed = False
        db_table = 'Word'
        app_label = APP_LABEL

    objects = models.Manager()
    words = WordsManager()
