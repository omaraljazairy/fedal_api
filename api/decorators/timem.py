import logging
from django.conf import settings
from datetime import datetime
#from memory_profiler import profile
from sys import getsizeof

logger = logging.getLogger(settings.AWS_LOGGER_NAME)

def time_memory(func):
    """Returns the execution time and and memory usage of a function. """
    def wrapper(*args, **kwargs):
        t1 = datetime.now()
        data = func(*args, **kwargs)
        t2 = datetime.now()
        total_time = 'decorator - Total time: {}'.format(t2 - t1)

        logger.debug("decorator - function size: %s" % getsizeof(data))
        logger.debug("decorator - function return type: %s" % type(data))
        logger.debug(total_time)
        return data
    return wrapper
