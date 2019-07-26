from .base import *

STATICFILES_DIRS = (
    os.path.join('static'),
    os.path.join(BASE_DIR, "static/"),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fbahamondes@hipodromochile.cl'
EMAIL_HOST_PASSWORD = 'pASSword2015'
EMAIL_PORT = 587