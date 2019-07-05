from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.10.10.85']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'intranet_externos',
        'USER': 'admin_hch',
        'PASSWORD': 'pass.1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}