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

DB_Test = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'fedal_api',
    'USER': 'test',
    'PASSWORD': 'thestester2020', #'nRNGRF7bjnJcUnCj',
    'HOST1': '172.20.0.3',
    'PORT': 3307
}

DB2 = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'fedal_api',
    'USER': 'api',
    'PASSWORD': 'Centos7_2020',
    'HOST': 'fedal.nl',
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
# fedal_api_api_1 714cc1299cba
# fedal_api_nginx_1 655798e7887f
# db_phpmyadmin_1 ba74e983accd
# db_mysql-server_1 554613e0e98b