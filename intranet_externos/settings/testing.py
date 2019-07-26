from .base import *

STATICFILES_DIRS = (
    os.path.join('static'),
    os.path.join(BASE_DIR, "static/"),
)

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

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fbahamondes@hipodromochile.cl'
EMAIL_HOST_PASSWORD = 'pASSword2015'
EMAIL_PORT = 587