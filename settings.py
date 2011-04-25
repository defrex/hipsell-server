# Django settings for rl project.

import os, sys
from coat.settings import *

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEVELOPMENT = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Toronto'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = False
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ew+k)=_@lmSDGRF$#2534rfsdaf$%#45trgsfrdg%$^#$%TYy$&f&#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cors.middleware.CORSMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'south',
    'sorl.thumbnail',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'coat',
    'javascript',
    'listings',
    'cors',
    'django_ses',
)

JS_DIR = os.path.join(MEDIA_ROOT, 'js')

COAT_COMPILERS = {
    'scss': ('css', 'sass %(source)s %(target)s'),
}

#for gmail email
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'aron@hipsell.com'
# EMAIL_HOST_PASSWORD = 'xcGc4Yzb'
# EMAIL_PORT = 587

#for Amazon SES. Disabled for now.
AWS_ACCESS_KEY_ID = 'AKIAIXYU57QQHZBDSB2A'
AWS_SECRET_ACCESS_KEY = '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'
EMAIL_BACKEND = 'django_ses.SESBackend'

from settings_local import *
