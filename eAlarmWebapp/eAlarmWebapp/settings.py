"""
Django settings for eAlarm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'scbnibhp&we2%yp@7vpl3ax8d37ccobx&sa06&mpifp$r5jsut'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'eAlarmWebapp.urls'

WSGI_APPLICATION = 'eAlarmWebapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eAlarm',
        'PORT': '9999',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '113322',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

LOGIN_REDIRECT_URL = '/home'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/common"
REPORT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/report"
TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
                os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'myapp/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS =(
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.csrf',
    'myapp.util.context_processors.deviceSummary',
    'django.core.context_processors.request',
)

ALARM_SERVER = 'http://localhost/AlarmServer/'
REPORT_SERVICE = 'ReportService'
PERMISSION_SERVICE = 'AuthorizationService'

LOCALE_PATHS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/locale", # replace with correct path here
)
LANGUAGES = (
    ('en', 'English'),
    ('vi', 'VietNamese'),
    ('de', 'Germany'),
    ('ja','Japanese')
)