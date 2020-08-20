# todo
""" add this model to a later general app"""
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

class Client(models.Model):
    """clients who will have their own api-key. define
    the client name.
    """
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    lastUpdated = models.DateTimeField(auto_now=True)


class ClietAPIKey(AbstractAPIKey):
    """ associate the client with the api-key. """

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = 'Client API-Key'
        verbose_name_plural = 'Client API-Keys'
