import os
from .site_settings.internationalization import *
from .site_settings.applist import *
from .site_settings.json_settings import get_settings
from .site_settings.staticfiles import *
from .site_settings.mediafiles import *
from .site_settings.mailserver import *
from .site_settings.logger_settings import *

settings = get_settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = settings['SECRET_KEY']
DEBUG = settings['DEBUG']
ALLOWED_HOSTS = settings['SECURITY']['ALLOWED_HOSTS']
DATABASES = settings['DB']

AUTH_USER_MODEL = 'common.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_intranet_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_intranet_base.wsgi.application'

AUTH_PASSWORD_VALIDATORS = settings['AUTH_PASSWORD_VALIDATORS']

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/login/'
