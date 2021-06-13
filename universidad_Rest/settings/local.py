from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'universidad',
        'USER': 'postgres',
        'PASSWORD': 'guerreretto9',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

