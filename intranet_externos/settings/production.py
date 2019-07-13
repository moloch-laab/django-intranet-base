from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['138.255.100.181']

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