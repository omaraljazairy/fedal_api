"""Main View classes for the Spanglish app."""

from .models import Word, Category
from .serializers import WordSerializer, CategorySerializer
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.permissions import IsOwner
from api.throttles import SpanglishRateThrottle
from django.conf import settings
from django.core.cache import cache
import logging


CACHE_TTL = getattr(settings, 'CACHE_TTL', 10)
logger = logging.getLogger('spanglish')


class CategoryViews(viewsets.ModelViewSet):
    """uses the ModelViewSet as there is nothing special about
    the views of the category. all standard CRUD operations."""

    permissions_classes = (IsAuthenticatedOrReadOnly, )
    # throttle_classes = (SpanglishRateThrottle, )
    # throttle_scope = 'spanglish'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    name = 'category-list'


class WordListView(generics.ListAPIView):
    """Containes the get request only for the Words."""

    permissions_classes = (IsAuthenticatedOrReadOnly, )
    # throttle_classes = (SpanglishRateThrottle, )
    # throttle_scope = 'spanglish'
    name = "words-list"
    queryset = Word.objects.all()

    def get(self, request, iso1):
        """Return a list of all words based on the iso1 param."""
        logger.debug("iso1 param received: %s" % iso1)

        queryset = Word.words.get_all_words_by_language(iso1=iso1)
        serializer = WordSerializer(queryset, many=True)
        data = serializer.data

        logger.debug("data returned from serializer: %s" % data)

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
