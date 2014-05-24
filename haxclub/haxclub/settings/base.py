from __future__ import absolute_import
import os
import sys
import socket
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

from unipath import Path

def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

def get_boolean_env_variable(var_name,default=None):
    try:
        value = get_env_variable(var_name)
    except ImproperlyConfigured:
        if type(default) == bool:
            return default
        else:
            raise

    if value is True or value.lower() == 'true' or value == '1' or value ==  1:
        return True
    return False

BASE_DIR = Path(__file__).ancestor(3)

HOSTNAME = socket.gethostname()
SITE_URL = get_env_variable('SITE_URL')

ALLOWED_HOSTS = [
    'localhost',
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

BROKER_URL = get_env_variable('BROKER_URL')

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# overwrite in each env settings
CELERYBEAT_SCHEDULE = {}

# get absolute path of current directory (useful for making project path more independent in development)

DEBUG = False
MAINTENANCE = get_boolean_env_variable('MAINTENANCE',False)

TEMPLATE_DEBUG = DEBUG
TESTING = 'test' in sys.argv

ADMINS = (
    ('John Salvatore', 'admin@hax.club'),
)

MANAGERS = ADMINS

CACHE_LOCATION = get_env_variable('CACHE_LOCATION')
CACHES = {
    'default': {
        'BACKEND': 'memcached.MemcachedCache',
        'LOCATION': CACHE_LOCATION,
		}
	}
DEFAULT_CACHE_EXPIRY = 60*15

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'haxclub'
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_S3_URL_PROTOCOL = 'https'

SECRET_KEY = get_env_variable('SECRET_KEY')

S3_URL = 'https://s3.amazonaws.com/{0}/'.format(AWS_STORAGE_BUCKET_NAME)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_HOST'),
        'PORT': get_env_variable('DATABASE_PORT'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BASE_DIR.child('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = BASE_DIR.child('static')


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    # for use with any static directories other than '<appname>/static'
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django_geoip.middleware.LocationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'django.middleware.gzip.GZipMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    # depends on settings.SITE_URL, which depends on env var
)

ROOT_URLCONF = 'haxclub.urls'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS = (
    # for user with any path other than '<appname>/templates'
)

INSTALLED_APPS = (
    'auth',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    #'django.contrib.humanize',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'djsupervisor',
    'rest_framework',
)

# This must be first. Do not move this.
INSTALLED_APPS = ('longerusername',) + INSTALLED_APPS

# django social-registration values
AUTHENTICATION_BACKENDS = (
    # this is the default backend, don't forget to include it!
    'django.contrib.auth.backends.ModelBackend',
)

EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'admin@hax.club'
EMAIL_USE_TLS = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

GRAPPELLI_ADMIN_TITLE = 'HaxClub - Admin'
GRAPPELLI_SWITCH_USER = True
