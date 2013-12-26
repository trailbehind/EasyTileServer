# Django settings for easyTileServer project.

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(PROJECT_DIR)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'tileserver',
        'USER': 'tileserver',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

UPLOAD_DIR = "uploads/"

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
TIME_ZONE = 'Etc/GMT'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'h%_uwd-d(18(8_**yj(t)^-2$2_az+5bv9gs@(hp8a5)kbife%'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'easyTileServer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'easyTileServer.wsgi.application'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.admin',
    'gunicorn',
    'rest_framework',
    'layers',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
}

TILESTACHE_CACHE = {"name":"Disk", "path":"/tmp/tilecache/", "umask":"0000"}

#import per-app settings to override defaults, before setting up logging
#to override log dir
LOG_DIR = os.path.join(os.path.dirname(PARENT_DIR), 'logs')

try:
    from easyTileServer.local_settings.py import *
except:
    pass

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'no_name': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'django_request.log'),
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'no_name',
        },
        'database': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_db.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'no_name',
        },
        'authenticate': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_auth.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'no_name',
        },
        'mail_admins': {
            'level':'ERROR',
            'class':'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'error_log': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_error.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['database', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'remoteAuthentication': {
            'handlers': ['authenticate', 'mail_admins', 'error_log'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
