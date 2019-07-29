from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_intranet_base',
        'USER': 'admin_hch',
        'PASSWORD': 'E;_9jpXK',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fbahamondes@hipodromochile.cl'
EMAIL_HOST_PASSWORD = 'pASSword2015'
EMAIL_PORT = 587

STATIC_ROOT = os.path.join(BASE_DIR, "static/")