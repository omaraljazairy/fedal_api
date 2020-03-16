"""Main View classes for the Spanglish app."""

from .models import Word
from .serializers import WordSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.permissions import IsOwner
from api.throttles import SpanglishRateThrottle
from django.conf import settings
from django.core.cache import cache
import logging


CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
LOGGER = logging.getLogger('spanglish')


class WordListView(generics.ListAPIView):
    """Containes the get request only for the Words."""

    permissions_classes = (IsAuthenticatedOrReadOnly, )
    throttle_classes = (SpanglishRateThrottle, )
    throttle_scope = 'spanglish'
    name = "words-list"
    queryset = Word.objects.all()

    def get(self, request, iso1):
        """Return a list of all words based on the iso1 param."""
        LOGGER.debug("iso1 param received: %s" % iso1)

        queryset = Word.words.get_all_words_by_language(iso1=iso1)
        serializer = WordSerializer(queryset, many=True)
        data = serializer.data

        LOGGER.debug("data returned from serializer: %s" % data)

        return Response(data, status=status.HTTP_200_OK)


class ApiRoot(generics.GenericAPIView):
    """Spanglish apis."""

    name = 'api-root'
    _ignore_model_permissions = True

    def get(self, request, *args, **kwargs):
        """Return all the apis."""
        return Response(
            {
            }
        )
