import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['43.200.252.76', "web", "localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_django',
        'USER': 'postgres',
        'PASSWORD': '0000',
        'HOST': 'db',  # docker-compose 서비스 이름
        'PORT': '5432',
    }
}
    