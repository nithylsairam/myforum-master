from myforum.settings import *
from myforum.emailer.settings import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Django debug flag.
DEBUG = True

# Should the site allow signup.
ALLOW_SIGNUP = False

# Private key used to validate external logins. Must be changed in production
LOGIN_PRIVATE_KEY = "private-key"

ADMINS = [
    ("Admin User", "admin@localhost")
]

# The password for admin users. Must be changed in production.
DEFAULT_ADMIN_PASSWORD = "admin@localhost"

# Shortcut to first admin information.
ADMIN_NAME, ADMIN_EMAIL = ADMINS[0]

# The default sender name on emails.
DEFAULT_FROM_EMAIL = f"{ADMIN_NAME} <{ADMIN_EMAIL}>"

# In MB
MAX_UPLOAD_SIZE = 10

MESSAGES_PER_PAGE = 5

# Set RECAPTCH keys here.
RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

# Django allauth settings.
SOCIALACCOUNT_EMAIL_VERIFICATION = None
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True


# Other settings
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[bioc] "
ACCOUNT_PASSWORD_MIN_LENGHT = 6
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"

LOGIN_REDIRECT_URL = "/"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

SOCIALACCOUNT_ADAPTER = "myforum.accounts.adapter.SocialAccountAdapter"

ACCOUNTS_APPS = [

    # Accounts configuration.
    'myforum.accounts.apps.AccountsConfig',

    # Allauth templates come last.
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

# Should the server look up locations in a task.
LOCATION_LOOKUP = False

INSTALLED_APPS = DEFAULT_APPS + ACCOUNTS_APPS + EMAILER_APP

AUTHENTICATION_BACKENDS += ["allauth.account.auth_backends.AuthenticationBackend"]

ROOT_URLCONF = 'myforum.accounts.urls'

# List of social login clients tuples.
# ( name, client_id, secret )

# Default clients redirect to localhost.
# Default clients may not be operational. See the
# django allauth documentation on how to set them up.

#
# Callback example settings:
#
# http://localhost:8000/accounts/social/google/login/callback/
# http://localhost:8000/accounts/social/github/login/callback/
#
SOCIAL_CLIENTS = [
    ("Google", "A", "B"),
    ("GitHub", "A", "B")
]
