"""
main configuration values for each environment.

This file will not e included in git.
"""
import os

ENV = 'DEV'
LEVEL = 'DEBUG'
DEBUG = True

LOG_DIR = os.getcwd() + '/logs/'

SECRET_KEY = 'y9QvbugUpoN5zRctfl0ZBpYE2iZoOJ2z'

DB = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'fedal_api',
    'USER': 'docker',
    'PASSWORD': 'dockerdev2020', #'nRNGRF7bjnJcUnCj',
    'HOST': '172.21.0.2',
    'PORT': 3306
}

REDIS_LOCATION = 'redis://192.168.192.26:6379/0'
REDIS_PASSWORD = 'mytestpass'
HOSTS = ['0.0.0.0',
         '192.168.192.29',
         '127.0.0.1',
         'fedal.net',
         'localhost',
         '192.168.178.25',
         '192.168.178.26',
         ]

# email service configs
EMAIL = {
    'hosts': {
        'strato': {
            "host": "smtp.strato.com",
            "port": 587,
            "secure": False,
            "tls": True
        },
    },
    "users": {
        'order_wcd': {
            "user": "order@wipecardetailing.nl",
            "pass": "knhxGGjB4EUJDR6h"
        }
    },
}
