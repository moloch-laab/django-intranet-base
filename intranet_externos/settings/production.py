from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['138.255.100.181']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'intranet_externos',
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