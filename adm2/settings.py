# -*- coding: utf-8 -*-

# Django settings for adm2 project.
from datetime import datetime
import os.path
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jittat Fakcharoenphol', 'jittat@gmail.com'),
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'onlineadmission_local54',                      # Or path to database file if using sqlite3.
#        'USER': 'onlineadmission',                      # Not used with sqlite3.
#        'PASSWORD': 'o-adm-for-dev',                  # Not used with sqlite3.
        'NAME': 'admnew',                      # Or path to database file if using sqlite3.
        'USER': 'admnew',                      # Not used with sqlite3.
        'PASSWORD': 'TbmQFy7j9FBVfN3N',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Bangkok'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'th'
LANGUAGE_CODE = 'th'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
#USE_I18N = True
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
#USE_L10N = True
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'media'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '45awn=0^h1^7eh5(l3r9wrq=_3)=_89a_mq8vo9-xe$&6l)aso'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'adm2.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'adm2.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',

    'south',
    'debug_toolbar',
    'mailer',

    'commons',
    'application',
    #'upload',
    'result',
    'review',
    'confirmation',
    'quota',
    #'feature_switch',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
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

FORMAT_MODULE_PATH = 'adm2.formats'

##########################################################

# --------------
# general settings

ADMISSION_YEAR = 2556
APPLICANT_TICKET_PREFIX = 2

ACCEPT_ONLY_GRADUATED = False
VERIFIY_MINIMUM_SCORE = False

# maximum number of choices
MAX_MAJOR_RANK = 1

# deadlines
SUBMISSION_DEADLINE = datetime(2012,11,6,0,0)

# payment
PAYMENT_DEADLINE_DISPLAY = datetime(2012,11,5)
ADMISSION_PAYMENT = 300
ADMISSION_PAYMENT_TEXT = u'สามร้อยบาทถ้วน'

# to distinguish payments between direct adm and quota adm
TICKET_SYSTEM_SALT = 'quota'

# --------------
# web interface settings

LOGIN_ENABLED = True
NAT_ID_VERIFICATION = True

MAX_PASSWORD_REQUST_PER_DAY = 10
MAX_DOC_UPLOAD_PER_DAY = 100

HTTP_BASE_PATH = 'http://localhost:8000'

FAKE_SENDING_EMAIL = True

SEND_MAILS_THROUGH_DJANGO_MAILER = False

EMAIL_BACKEND = 'commons.backends.smtp.EmailBackend'

EMAIL_HOST = 'nontri.ku.ac.th'
EMAIL_HOST_USER = 'jtf'
EMAIL_HOST_PASSWORD = 'xxxxxxxx'
EMAIL_SENDER = 'KU Eng Admission Team <jtf@ku.ac.th>'

SHOW_SCORE_IMPORT_STATUS = False

SHOW_CLEARING_HOUSE_RESULT = False

# used in redirect_to_index
INDEX_PAGE = 'start-page'

# ---------------
# web system settings

UPLOADED_DOC_PATH = os.path.join(PROJECT_DIR,'data/upload')
MAX_UPLOADED_DOC_FILE_SIZE = 2000000

# ------------------
# result mails

ADM_RESULT_MAIL_SUBJECT = ''
ADM_RESULT_MAIL_BUILD_BODY = None

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

try:
    from settings_local import *
except ImportError:
    pass 
