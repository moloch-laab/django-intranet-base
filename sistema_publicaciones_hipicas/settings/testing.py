from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['10.10.10.85']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sistema_publicaciones_hipicas',
        'USER': 'admin_hch',
        'PASSWORD': 'pass.1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATICFILES_DIRS.append('/home/sistema_publicaciones_hipicas/sistema_publicaciones_hipicas/static/')