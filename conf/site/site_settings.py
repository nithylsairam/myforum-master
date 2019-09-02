from myforum.settings import *

# Enable the right settings.

from myforum.forum.settings import *

#from myforum.forum.settings import *

import logging

logger = logging.getLogger("myforum")

DEBUG = True

SITE_ID = 1
SITE_DOMAIN = "www.lvh.me"
SITE_NAME = "myforum Engine"

HTTP_PORT = ''
PROTOCOL = 'http'

#ALLOWED_HOSTS = [SITE_DOMAIN]

WSGI_APPLICATION = 'conf.site.site_wsgi.application'

try:
    # Attempts to load site secrets.
    from .site_secrets import *

    logger.info("Imported settings from .site_secrets")
except ImportError as exc:
    logger.warn(f"No secrets module could be imported: {exc}")
