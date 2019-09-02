"""
Common settings that are applicable to all myforum apps.
"""

import os

# The logging configuration
from myforum.logconf import LOGGING

# Helper function for building absolute paths.
def join(*args):
    return os.path.abspath(os.path.join(*args))


# Set the home page to the engine or forum
INTERNAL_IPS = ['127.0.0.1']

# Admin users will be created automatically with DEFAULT_ADMIN_PASSWORD.
ADMINS = [
    ("Admin User", "admin@localhost")
]

# Shortcut to first admin information.
ADMIN_NAME, ADMIN_EMAIL = ADMINS[0]

# The default sender name on emails.
DEFAULT_FROM_EMAIL = f"{ADMIN_NAME} <{ADMIN_EMAIL}>"

# The current directory path.
__CURR_DIR = os.path.dirname(join(__file__))

# The directory relative to which all content is stored.
BASE_DIR = join(__CURR_DIR, "..")

# Django debug flag.
DEBUG = True

# Default installed apps.
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mailer',
    'compressor',
    'taggit',
    'snowpenguin.django.recaptcha2',
    'rest_framework',
    'debug_toolbar',
]

# Enabled apps.
INSTALLED_APPS = DEFAULT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Site specific information
SITE_ID = 1
SITE_DOMAIN = "localhost"
SITE_NAME = "myforum Engine"

# Deployment specific parameters.
PROTOCOL = "http"
HTTP_PORT = '8000'
BASE_URL = f"{PROTOCOL}://{SITE_DOMAIN}:{HTTP_PORT}"

# Change this in production!
SECRET_KEY = 'secret-key'

# Change this in production!
API_KEY = "api-key"

# Template specific settings.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'string_if_invalid': "**MISSING**",
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'myforum.context.main',
            ],
            # 'loaders': [
            #     ('django.template.loaders.cached.Loader',
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #     )
            # ]
        },
    },
]

# Authentication backend.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# The WSGI application.
WSGI_APPLICATION = 'myforum.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

]

# Database settings.
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASE_NAME = os.environ.setdefault("DATABASE_NAME", "database.db")
DATABASE_NAME = join(BASE_DIR, 'export', 'db', DATABASE_NAME)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_NAME,
    }
}

ALLOWED_HOSTS = ['www.lvh.me', 'localhost', '127.0.0.1']

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Configure language detection
LANGUAGE_DETECTION = ['en']

# The static URL start.
STATIC_URL = '/static/'

# The static root directory.
STATIC_ROOT = join(BASE_DIR, 'export', 'static')

# Global directories for static files.
STATICFILES_DIRS = [
    join(BASE_DIR, "myforum", "static"),
]

# The media URL start.
MEDIA_URL = '/media/'

# The media root directory.
MEDIA_ROOT = join(BASE_DIR, 'export', 'media')


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]

# Apply default logger setting.
LOGGER_NAME = "myforum"

# The email delivery engine.
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'sparkpost.django.email_backend.SparkPostEmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Session engine.
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Session key name.
SESSION_KEY = "session"
