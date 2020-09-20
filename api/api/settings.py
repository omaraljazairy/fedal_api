"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from pathlib import Path
import datetime
from boto3.session import Session

# create a base dir constant that points to the main project directoy
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# use pathlib to create the path for the env.py file and load it if it
# exists, otherwise just ignore it and take the environment variables from
# the system
env_file = Path(BASE_DIR, "api/env.py")
if os.path.isfile(env_file):
    from api import env

# check if the logs directory exsts, if not, create it
log_dir = Path(BASE_DIR, "logs")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# print("os env: %s" % os.environ)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# check if the environ variables are set for the elasticbean environment.
# if not, use the local env file.

LEVEL = os.environ['LEVEL']
DEBUG = os.environ['DEBUG']
ENV = os.environ['ENV']
IS_TESTING = False
ALLOWED_HOSTS = os.environ['HOSTS'].split(',')

# AWS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_REGION_NAME = os.environ['AWS_REGION_NAME']
AWS_LOG_GROUP = os.environ['AWS_LOG_GROUP'] # your log group
AWS_LOG_STREAM = os.environ['AWS_LOG_STREAM'] # your stream
AWS_LOGGER_NAME = os.environ['AWS_LOGGER_NAME'] # your logger

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'corsheaders',
    'drf_yasg',
    'rest_framework',
    'spanglish',
    'wipecardetailing',
    'rest_framework_api_key'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

# logger
boto3_session = Session(
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
  region_name=AWS_REGION_NAME
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s] \
             - [%(module)s:%(funcName)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'aws': {
            'format': "%(asctime)s %(levelname)s %(module)s: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join( os.environ['LOG_DIR'] ,'api.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'watchtower': {
            'level': 'DEBUG',
            'class': 'watchtower.CloudWatchLogHandler',
            'boto3_session': boto3_session,
            'log_group': AWS_LOG_GROUP,
            'stream_name': AWS_LOG_STREAM,
            'formatter': 'aws', # use custom format
        },
    },
    'loggers': {
        'spanglish': {
            'handlers': ['file'],
            'level': LEVEL,
            'propagate': True,
        },
        'wipecardetailing': {
            'handlers': ['file'],
            'level': LEVEL,
            'propagate': True,
        },
        'api': {
            'handlers': ['file'],
            'level': LEVEL,
            'propagate': True,
        },
        'email': {
            'handlers': ['file'],
            'level': LEVEL,
            'propagate': True,
        },
        AWS_LOGGER_NAME: {
            'level': 'DEBUG',
            'handlers': ['watchtower'] if ENV != 'DEV' else ['file'],
            'propagate': False,
        },
    },
}


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ['RDS_DB_ENGINE'],
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_DB_USERNAME'],
        'PASSWORD': os.environ['RDS_DB_PASSWORD'],
        'HOST': os.environ['RDS_DB_HOST'],
        'PORT': os.environ['RDS_DB_PORT'],
    },
    'spanglish': {
        'ENGINE': os.environ['RDS_DB_ENGINE'],
        'NAME': 'Spanglish',
        'USER': os.environ['RDS_DB_USERNAME'],
        'PASSWORD': os.environ['RDS_DB_PASSWORD'],
        'HOST': os.environ['RDS_DB_HOST'],
        'PORT': os.environ['RDS_DB_PORT'],
    },
    'wipecardetailing': {
        'ENGINE': os.environ['RDS_DB_ENGINE'],
        'NAME': 'Wipecardetailing',
        'USER': os.environ['RDS_DB_USERNAME'],
        'PASSWORD': os.environ['RDS_DB_PASSWORD'],
        'HOST': os.environ['RDS_DB_HOST'],
        'PORT': os.environ['RDS_DB_PORT'],
    }
}


DATABASE_RAW_TABLES = {
    "category": " Spanglish.Category ",
    "language": "Spanglish.Language",
    "sentence": "Spanglish.Sentence",
    "translation": "Spanglish.Translation",
    "verb": "Spanglish.Verb",
    "word": "Spanglish.Word",
    "formsubmit": "Wipecardetailing.FormSubmits",
    "multimedia": "Wipecardetailing.Multimedia",
}

DATABASE_ROUTERS = [
    'spanglish.dbrouter.DBRouter',
    'wipecardetailing.dbrouter.DBRouter',
]

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S%z',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        #'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.IsAuthenticatedOrReadOnly',

    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        # 'api.throttles.SpanglishRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10000/day',
        'user': '10000/day',
        'spanglish': '100/day',
        'wipecardetailing': '100/day',
    },
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=1420),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.environ['SECRET_KEY'],
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=1420),
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# DATETIME_FORMAT = "%Y-%m-%d %H:%M:%s"
# DATETIME_FORMAT = 'N j, Y, p'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_DOWNLOAD_HOST = os.environ['DOWNLOAD_LINK_HOST']
DOWNLOAD_IMAGE_URI = MEDIA_DOWNLOAD_HOST + 'wipecardetailing' + MEDIA_URL
print("Media_download_host ", MEDIA_DOWNLOAD_HOST)

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = os.environ['EMAIL_STRATO_TLS']
EMAIL_HOST = os.environ['EMAIL_STRATO_HOST']
EMAIL_PORT = os.environ['EMAIL_STRATO_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_STRATO_WCD_ORDER_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_STRATO_WCD_ORDER_PASSWORD']
# EMAIL_USE_SSL = bool(os.environ['EMAIL_STRATO_SECURE'])
EMAIL_USE_TLS = bool(os.environ['EMAIL_STRATO_TLS'])
EMAIL_TO = os.environ['EMAIL_TO']
# API-Key
API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

CORS_ORIGIN_ALLOW_ALL =  True

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Basic': {
            'type': 'basic'
      },
      'Bearer': {
          'type': 'http',
          'scheme': 'bearer',
          'bearerFormat': 'JWT',
          'in': 'header'
      },
      'ApiKeyAuth': {
          'type': 'apiKey',
          'name': 'Authorization',
          'in': 'header'
      }
   }
}