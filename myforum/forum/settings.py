# Inherit from the main settings file.

# Inherit from the accounts settings file.
from myforum.accounts.settings import *

# Django debug flag.
DEBUG = True

# Show debug toolbar
DEBUG_TOOLBAR = False

# Override compression if needed.
# COMPRESS_ENABLED = True

POSTS_PER_PAGE = 40
USERS_PER_PAGE = 100
MESSAGES_PER_PAGE = 100
TAGS_PER_PAGE = 50


# Log the time for each request
TIME_REQUESTS = True

# Indexing interval in seconds.
INDEX_SECS_INTERVAL = 10
# Number of results to display.
SEARCH_LIMIT = 20

# Minimum amount of characters to preform searches
SEARCH_CHAR_MIN = 1

BATCH_INDEXING_SIZE = 1000

VOTE_FEED_COUNT = 10
LOCATION_FEED_COUNT = 5
AWARDS_FEED_COUNT = 10
REPLIES_FEED_COUNT = 15

SIMILAR_FEED_COUNT = 30

SESSION_UPDATE_SECONDS = 40

# Search index name
INDEX_NAME = os.environ.setdefault("INDEX_NAME", "index")
# Relative index directory
INDEX_DIR = os.environ.setdefault("INDEX_DIR", "search")
# Absolute path to index directory in export/
INDEX_DIR = os.path.abspath(os.path.join(MEDIA_ROOT, '..', INDEX_DIR))

SOCIALACCOUNT_EMAIL_VERIFICATION = None
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True

LOGIN_REDIRECT_URL = "/"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

SOCIALACCOUNT_ADAPTER = "myforum.accounts.adapter.SocialAccountAdapter"

FORUM_APPS = [
    'myforum.forum.apps.ForumConfig',
    'pagedown',

]

# Additional middleware.
MIDDLEWARE += [
    'myforum.forum.middleware.user_tasks',
    'myforum.forum.middleware.benchmark',
]

# Post types displayed when creating, empty list displays all types.
ALLOWED_POST_TYPES = []

# Enable debug toolbar specific functions
if DEBUG_TOOLBAR:
    FORUM_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')


# Import the default pagedown css first, then our custom CSS sheet
# to avoid having to specify all the default styles
PAGEDOWN_WIDGET_CSS = ('pagedown/demo/browser/demo.css', "lib/pagedown.css",)

INSTALLED_APPS = DEFAULT_APPS + FORUM_APPS + ACCOUNTS_APPS + EMAILER_APP

ROOT_URLCONF = 'myforum.forum.urls'

WSGI_APPLICATION = 'myforum.wsgi.application'

# Time between two accesses from the same IP to qualify as a different view.
POST_VIEW_MINUTES = 7

COUNT_INTERVAL_WEEKS = 10000

# This flag is used flag situation where a data migration is in progress.
# Allows us to turn off certain type of actions (for example sending emails).
DATA_MIGRATION = False

# Tries to load up secret settings from a predetermined module
# This is for convenience only!
try:
    from conf.run.secrets import *
    print(f"Loaded secrets from: conf.run.secrets")
except Exception as exc:
    print(f"Secrets module not imported: {exc}")
