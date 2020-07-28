"""Custom throttle clases for each app."""

from rest_framework.throttling import UserRateThrottle
import logging

logger = logging.getLogger('throttles')


class SpanglishRateThrottle(UserRateThrottle):
    """used for the Spanglish app with.

    Extends the userRateThrottle class and sets a
    scope attribute to spanglish.
    """

    logger.debug("throttle for spanglish users")
    scope = 'spanglish'


class WipecardetailingRateThrottle(UserRateThrottle):
    """used for the Wipecardetailing app with.

    Extends the userRateThrottle class and sets a
    scope attribute to spanglish.
    """

    logger.debug("throttle for wipecardetailing users")
    scope = 'wipecardetailing'
