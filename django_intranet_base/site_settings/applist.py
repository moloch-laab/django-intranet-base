BEFORE_DJANGO_APPS = (

)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'django_intranet_base.apps.common',
    'django_intranet_base.apps.core',
)

THIRD_PARTY_APPS = (
    'menu_generator',
    'fpdf',
    'simple_email_confirmation',
)


INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
