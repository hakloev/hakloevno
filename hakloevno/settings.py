"""
Django settings for hakloevno project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import inspect
import sys


def validate(keyset):
    """
    Verify that given the current run environment (LOCAL, STAGING or PRODUCTION), all necessary environment variables
    have been set, to override the defaults in this settings file.
    :return: An empty list if no violations were found, otherwise, a populated list of error strings.
    """

    if PRODUCTION:
        _env = 'PRODUCTION'
    elif STAGING:
        _env = 'STAGING'
    else:
        _env = 'LOCAL'

    print('Validating settings for current environment: %s (Debug: %s)' % (_env, DEBUG))

    _settings = inspect.getmodule(validate)
    _relevant = set(keyset) & set(dir(_settings))
    _errors = []
    for var in _relevant:
        if not getattr(_settings, var):
            _errors.append('ERROR: "%s" has not been set!' % var)

    return _errors


# Declare what environment we are operating in
PRODUCTION = 'HAKLOEVNO_PRODUCTION' in os.environ
STAGING = 'HAKLOEVNO_STAGING' in os.environ
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not PRODUCTION

# Define which attributes must be set if we are in staging
STAGING_CRITICALS = {
    'DB_NAME',
    'DB_USER',
    'DB_PASSWORD',
    'DB_HOST',
    'DB_PORT',
}
# Define which attributes must be set if we are in production
PRODUCTION_CRITICALS = STAGING_CRITICALS.copy()
PRODUCTION_CRITICALS.update({
    'SECRET_KEY',
    'SESSION_COOKIE_SECURE',
    'CSRF_COOKIE_SECURE',
    'CSRF_COOKIE_HTTPONLY',
})

# Fetch values from environment, if provided
DB_NAME = os.getenv('HAKLOEVNO_DB_NAME', '')
DB_USER = os.getenv('HAKLOEVNO_DB_USER', '')
DB_PASSWORD = os.getenv('HAKLOEVNO_DB_PASSWORD', '')
DB_HOST = os.getenv('HAKLOEVNO_DB_HOST', '')
DB_PORT = os.getenv('HAKLOEVNO_DB_PORT', '')
SECRET_KEY = os.getenv('HAKLOEVNO_SECRET_KEY', '')

if PRODUCTION or STAGING:
    if PRODUCTION:
        _errors = validate(PRODUCTION_CRITICALS)
    else:
        _errors = validate(STAGING_CRITICALS)
    if _errors:
        for error in _errors:
            sys.stderr.write('%s\n' % error)
        sys.stderr.write(
            'Please set these environment variables in Environment/uWSGI/Gunicorn.\n'
        )
        sys.stderr.flush()
        sys.exit(1)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'hakloev.no']

DEFAULT_FROM_EMAIL = 'epona@hakloev.no'

ADMINS = (
    ('Håkon Ødegård Løvdal', 'me@hakloev.no'),
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_markdown',
    'apps.blog'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MARKDOWN_EXTENSIONS = [
    'markdown.extensions.codehilite',
    'markdown.extensions.extra',  # Tables, fenced code blocks etc
]

ROOT_URLCONF = 'hakloevno.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'hakloevno', 'templates')],
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

WSGI_APPLICATION = 'hakloevno.wsgi.application'

# Define our database backend based on which environment we are in
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
if PRODUCTION or STAGING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'dev.db'),
        }
    }

if PRODUCTION or STAGING:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = 'DENY'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'files/dist'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s.%(funcName)s:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'WARNING',
        },
        'apps.authentication': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}