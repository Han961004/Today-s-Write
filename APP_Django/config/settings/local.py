import os
from .base import *  # 이걸로 base 상속받아서 사용한다. 

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_django',
        'USER': 'postgres',
        'PASSWORD': '0000',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
