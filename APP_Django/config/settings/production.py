import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['43.200.252.76', "web", "localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'app_django'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '0000'),
        'HOST': os.environ.get('DATABASE_HOST', 'django_db'),  # 여기 수정!
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
    