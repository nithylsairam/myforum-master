# Import all common settings.
from myforum.settings import *

# Additional apps enabled.
EMAILER_APP = [
    'myforum.emailer.apps.EmailerConfig'
]

INSTALLED_APPS = DEFAULT_APPS + EMAILER_APP

# The url specification.
ROOT_URLCONF = 'myforum.emailer.urls'

# This flag is used flag situation where a data migration is in progress.
# Allows us to turn off certain type of actions (for example sending emails).
DATA_MIGRATION = False
