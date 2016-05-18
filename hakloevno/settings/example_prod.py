from hakloevno.settings.base import *

ALLOWED_HOSTS = ['hakloev.no']

SECRET_KEY = 'secret'

DEBUG = False

ADMINS = (
    ('Håkon Ødegård Løvdal', 'me@hakloev.no'),
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# Define our database backend based on which environment we are in
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',  # Database name
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

